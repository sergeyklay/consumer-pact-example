# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest
from consumer.product import ProductConsumer

pytest_plugins = [
    'pact_fixtures'
]


@pytest.fixture
def consumer(mock_opts) -> ProductConsumer:
    return ProductConsumer(
        f"http://{mock_opts['host_name']}:{mock_opts['port']}"
    )
