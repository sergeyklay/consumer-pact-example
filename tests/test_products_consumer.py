# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Pact test for Product service client"""

import logging
import os
from pact import Consumer, Like, Provider, Term, Format
import pytest
import atexit

from consumer.product import ProductConsumer

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# If publishing the Pact(s), they will be submitted to the Pact Broker here.
# For the purposes of this example, the broker is started up as a fixture defined
# in conftest.py. For normal usage this would be self-hosted or using PactFlow.
PACT_BROKER_URL = 'http://localhost'
PACT_BROKER_USERNAME = 'pactbroker'
PACT_BROKER_PASSWORD = 'pactbroker'

# Define where to run the mock server, for the consumer to connect to. These
# are the defaults so may be omitted
PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 1234

# Where to output the JSON Pact files created by any tests
PACT_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def consumer() -> ProductConsumer:
    return ProductConsumer(f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}')


@pytest.fixture(scope='session')
def pact(request):
    """Set up a Pact Consumer, which provides the Provider mock service.

    This will generate and optionally publish Pacts to the Pact Broker"""

    # When publishing a Pact to the Pact Broker, a version number of the Consumer
    # is required, to be able to construct the compatability matrix between the
    # Consumer versions and Provider versions
    version = request.config.getoption('--publish-pact')
    publish = True if version else False

    pact = Consumer('ProductServiceClient', version=version).has_pact_with(
        Provider('ProductService'),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR,
        publish_to_broker=publish,
        broker_base_url=PACT_BROKER_URL,
        broker_username=PACT_BROKER_USERNAME,
        broker_password=PACT_BROKER_PASSWORD,
    )

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


def test_get_product(pact, consumer):
    # Define the Matcher; the expected structure and content of the response
    expected = {
    }

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a body which is
    # "Like" the structure defined above. This means the mock provider will
    # return the EXACT content where defined, e.g. Product_X for title, and
    # SOME appropriate content e.g. for description.
    (
        pact.given('there is a product with ID 1')
            .upon_receiving('a request for a product')
            .with_request('get', '/v1/products/1')
            .will_respond_with(200, body=Like(expected))
    )

    with pact:
        # Perform the actual request
        product = consumer.get_product(1)

        # In this case the mock Provider will have returned a valid response
        assert product.title == 'Product_X'

        # Make sure that all interactions defined occurred
        pact.verify()
