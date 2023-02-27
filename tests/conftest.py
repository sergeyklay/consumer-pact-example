# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import os
import subprocess

import pytest

from consumer import __version__ as version
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


def git_revision_short_hash() -> str:
    """Get the short Git commit."""
    root_dir = os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )

    return subprocess.check_output(
        ['git', '-C', root_dir, 'rev-parse', '--short', 'HEAD']
    ).decode('ascii').strip()


@pytest.fixture(scope='session')
def app_version() -> str:
    """Get participant version number.

    To get the most out of the Pact Broker, it should either be the git sha
    (or equivalent for your repository), be a git tag name, or it should
    include the git sha or tag name as metadata if you are using semantic
    versioning eg. 1.2.456+405b31ec6.

    See https://docs.pact.io/pact_broker/pacticipant_version_numbers for more
    details."""
    git_commit = git_revision_short_hash()
    return f'{version}+{git_commit}'
