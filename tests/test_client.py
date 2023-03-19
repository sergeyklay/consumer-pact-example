# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Unit test for Product service client."""

from consumer.client import Client


def test_custom_options():
    client = Client()
    assert client.options == {
        'base_url': 'http://localhost',
        'max_retries': 3,
        'timeout': 5.0,
    }

    client = Client(foo='1', bar='2', baz='3')
    assert client.options == {
        'bar': '2',
        'base_url': 'http://localhost',
        'baz': '3',
        'foo': '1',
        'max_retries': 3,
        'timeout': 5.0,
    }
