# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Unit test for Product service client."""

from consumer.product import Client


def test_custom_options():
    client = Client()
    assert client.options == {
        'base_url': 'http://localhost',
        'version': 'v1',
    }

    client = Client(foo='1', bar='2', baz='3')
    assert client.options == {
        'bar': '2',
        'base_url': 'http://localhost',
        'baz': '3',
        'foo': '1',
        'version': 'v1',
    }
