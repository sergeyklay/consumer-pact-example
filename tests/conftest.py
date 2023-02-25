# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import os

import pytest

from consumer.product import ProductConsumer


@pytest.fixture(scope='session')
def mock_opts():
    """Define where to run the mock server, for the consumer to connect to."""
    host_name = os.environ.get('PACT_MOCK_HOST', 'localhost')
    return {
        'host_name': host_name.rstrip('/'),
        'port': int(os.environ.get('PACT_MOCK_PORT', 1234)),
    }


@pytest.fixture(scope='session')
def pact_dir():
    """Get path to output the JSON Pact files created by any tests."""
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'pacts'
    )


@pytest.fixture
def consumer(mock_opts) -> ProductConsumer:
    return ProductConsumer(
        f"http://{mock_opts['host_name']}:{mock_opts['port']}"
    )
