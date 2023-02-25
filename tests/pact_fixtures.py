# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import atexit
import logging
import os

import docker
import pytest
from pact import Consumer, Provider
from testcontainers.compose import DockerCompose

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


# This fixture is to simulate a managed Pact Broker or PactFlow account.
# For almost all purposes outside this example, you will want to use a real
# broker. See https://github.com/pact-foundation/pact_broker for further details.
@pytest.fixture(scope='session', autouse=True)
def broker(request):
    version = request.config.getoption('--publish-pact')
    publish = True if version else False

    # If the results are not going to be published to the broker, there is
    # nothing further to do anyway
    if not publish:
        yield
        return

    run_broker = request.config.getoption('--run-broker')

    if run_broker:
        # Start up the broker using docker-compose
        log.info('Starting broker')
        broker = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'broker'
        )
        with DockerCompose(broker, pull=True) as compose:
            stdout, stderr = compose.get_logs()
            if stderr:
                log.error(f'Errors\n:{stderr}')
            log.info(f'{stdout}')
            log.info('Started broker')

            yield

            log.info('Stopping broker')
        log.info('Broker stopped')
    else:
        # Assuming there is a broker available already, docker-compose has been
        # used manually as the --run-broker option has not been provided
        yield
        return


@pytest.fixture(scope='session')
def pact_settings():
    return dict(
        # If publishing the Pact(s), they will be submitted to the Pact Broker here.
        # For the purposes of this example, the broker is started up as a fixture defined
        # in conftest.py. For normal usage this would be self-hosted or using PactFlow.
        broker_url=os.environ.get(
            'PACT_BROKER_URL',
            'http://localhost'
        ).rstrip('/'),
        broker_username=os.environ.get(
            'PACT_BROKER_USERNAME',
            'pactbroker'
        ),
        broker_password=os.environ.get(
            'PACT_BROKER_PASSWORD',
            'pactbroker'
        ),

        # Define where to run the mock server, for the consumer to connect to. These
        # are the defaults so may be omitted
        mock_host=os.environ.get(
            'PACT_MOCK_HOST',
            'localhost'
        ).rstrip('/'),
        mock_port=int(os.environ.get('PACT_MOCK_PORT', 1234)))


@pytest.fixture(scope='session', autouse=True)
def publish_existing_pact(broker, pact_settings):
    source = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'pacts'
    )
    pacts = [f'{source}:/pacts']
    envs = {
        # Keep these parameters according to docker-compose.yml
        'PACT_BROKER_BASE_URL': 'http://broker_app:9292',
        'PACT_BROKER_USERNAME': pact_settings['broker_username'],
        'PACT_BROKER_PASSWORD': pact_settings['broker_password'],
    }

    client = docker.from_env()

    log.info('Publishing existing Pact')

    # The following code will execute something like this:
    #
    #    docker run -ti \
    #      --rm \
    #      -v "$(pwd)"/tests/pacts:/pacts \
    #      -e PACT_BROKER_BASE_URL='http://broker_app:9292' \
    #      -e PACT_BROKER_USERNAME=pactbroker \
    #      -e PACT_BROKER_PASSWORD=pactbroker \
    #      --network broker_backend \
    #      pactfoundation/pact-cli:latest \
    #      publish /pacts --consumer-app-version 1
    #
    client.containers.run(
        remove=True,
        # See docker-compose.yml for docker network name
        network='broker_backend',
        volumes=pacts,
        image='pactfoundation/pact-cli:latest',
        environment=envs,
        command='publish /pacts --consumer-app-version 1')

    log.info('Finished publishing')


@pytest.fixture(scope='session')
def pact(request, pact_settings):
    """Set up a Pact Consumer, which provides the Provider mock service.

    This will generate and optionally publish Pacts to the Pact Broker"""

    # When publishing a Pact to the Pact Broker, a version number of the Consumer
    # is required, to be able to construct the compatability matrix between the
    # Consumer versions and Provider versions
    version = request.config.getoption('--publish-pact')
    publish = True if version else False

    # Where to output the JSON Pact files created by any tests
    pact_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'pacts'
    )

    consumer = Consumer('ProductServiceClient', version=version)
    pact = consumer.has_pact_with(
        Provider('ProductService'),
        host_name=pact_settings['mock_host'],
        port=pact_settings['mock_port'],
        pact_dir=pact_dir,
        publish_to_broker=publish,
        broker_base_url=pact_settings['broker_url'],
        broker_username=pact_settings['broker_username'],
        broker_password=pact_settings['broker_password'])

    pact.start_service()

    # Make sure the Pact mocked provider is stopped when we finish, otherwise
    # port 1234 may become blocked
    atexit.register(pact.stop_service)

    yield pact

    # This will stop the Pact mock server, and if publish is True, submit Pacts
    # to the Pact Broker
    pact.stop_service()

    # Given we have cleanly stopped the service, we do not want to re-submit the
    # Pacts to the Pact Broker again atexit, since the Broker may no longer be
    # available if it has been started using the --run-broker option, as it will
    # have been torn down at that point
    pact.publish_to_broker = False


def pytest_addoption(parser):
    parser.addoption(
        '--publish-pact',
        type=str,
        action='store',
        help='Upload generated pact file to pact broker with version'
    )

    parser.addoption(
        '--run-broker',
        type=bool,
        action='store',
        help='Whether to run broker in this test or not.',
    )

    parser.addoption(
        '--provider-url',
        type=str,
        action='store',
        help='The url to our provider.',
    )
