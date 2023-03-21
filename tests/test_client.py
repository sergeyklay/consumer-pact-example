# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Unit test for Product service client."""

import responses
from responses import POST

from consumer.client import Client, default_headers


@responses.activate
def test_default_headers(client):
    client.headers['key'] = 'value'
    url = f'{client.base_url}/v2/products'

    responses.add(POST, url, status=200, body='{}')

    client.post('/v2/products', {})
    headers = responses.calls[0].request.headers

    assert headers['key'] == 'value'
    assert headers['User-Agent'] == default_headers()['user-agent']
    assert headers['Accept'] == 'application/json'
    assert headers['Content-Type'] == 'application/json; charset=utf-8'


@responses.activate
def test_request_headers(client):
    url = f'{client.base_url}/v2/products'
    responses.add(POST, url, status=200, body='{}')

    client.post('/v2/products', {}, headers={
        'User-Agent': 'Test',
        'Content-Type': 'text/plain;charset=UTF-8'
    })

    headers = responses.calls[0].request.headers

    assert headers['User-Agent'] == 'Test'
    assert headers['Content-Type'] == 'text/plain;charset=UTF-8'


@responses.activate
def test_overriding_headers(client):
    client.headers['key1'] = 'value1'
    client.headers['key2'] = 'value2'

    url = f'{client.base_url}/v2/products'
    responses.add(POST, url, status=200, body='{}')

    client.post('/v2/products', {}, headers={'key1': 'value3'})
    headers = responses.calls[0].request.headers

    assert headers['key1'] == 'value3'
    assert headers['key2'] == 'value2'


def test_custom_options():
    client = Client()
    assert client.options == {
        'base_url': 'http://localhost',
        'max_retries': 3,
        'timeout': 5.0,
        'version': 'v2',
    }

    client = Client(foo='1', bar='2', baz='3')
    assert client.options == {
        'bar': '2',
        'base_url': 'http://localhost',
        'baz': '3',
        'foo': '1',
        'max_retries': 3,
        'timeout': 5.0,
        'version': 'v2',
    }
