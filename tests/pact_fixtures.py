# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest
import pathlib
import docker
import os
from testcontainers.compose import DockerCompose


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
        print('Starting broker')
        broker = str(pathlib.Path.cwd().joinpath(os.path.dirname(os.path.realpath(__file__)), 'broker').resolve())
        with DockerCompose(broker, pull=True) as compose:
            stdout, stderr = compose.get_logs()
            if stderr:
                print(f'Errors\n:{stderr}')
            print(f'{stdout}')
            print('Started broker')

            yield

            print('Stopping broker')
        print('Broker stopped')
    else:
        # Assuming there is a broker available already, docker-compose has been
        # used manually as the --run-broker option has not been provided
        yield
        return


@pytest.fixture(scope='session', autouse=True)
def publish_existing_pact(broker):
    source = str(pathlib.Path.cwd().joinpath('..', 'pacts').resolve())
    pacts = [f'{source}:/pacts']
    envs = {
        'PACT_BROKER_BASE_URL': 'http://broker_app:9292',
        'PACT_BROKER_USERNAME': 'pactbroker',
        'PACT_BROKER_PASSWORD': 'pactbroker',
    }

    client = docker.from_env()

    print('Publishing existing Pact')
    client.containers.run(
        remove=True,
        network='broker_default',
        volumes=pacts,
        image='pactfoundation/pact-cli:latest',
        environment=envs,
        command='publish /pacts --consumer-app-version 1',
    )

    print('Finished publishing')


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
