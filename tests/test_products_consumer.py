# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Pact test for Product service client."""

import atexit
import json
import logging

import pytest
from pact import Consumer, EachLike, Provider

from consumer.product import Client, Product
from .factories import (
    HeadersFactory,
    NotFoundErrorFactory,
    ProductFactory,
    url_term,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def mock_service(mock_opts, pact_dir, app_version):
    """Set up a Pact Consumer, which provides the Provider mock service."""
    consumer = Consumer('ProductServiceClient', version=app_version)
    mock_service = consumer.has_pact_with(
        Provider('ProductService'),
        pact_dir=pact_dir,
        **mock_opts,
    )

    # Start the Pact mock server
    mock_service.start_service()

    # Make sure the Pact mocked provider is stopped when we finish, otherwise
    # port 1234 may become blocked
    atexit.register(mock_service.stop_service)

    yield mock_service

    # This will stop the Pact mock server, and if publish is True, submit Pacts
    # to the Pact Broker
    mock_service.stop_service()

    # Given we have cleanly stopped the service, we do not want to re-submit
    # the Pacts to the Pact Broker again atexit, since the Broker may no longer
    # be available at that point
    mock_service.publish_to_broker = False


def test_get_existent_product(mock_service, client: Client):
    # Define the Matcher; the expected structure and content of the response
    expected = ProductFactory(name='product0')

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a body which is
    # "Like" the structure defined above. This means the mock provider will
    # return the EXACT content where defined, e.g. 'product0' for name, and
    # SOME appropriate content e.g. for description.
    (mock_service
     .given('there is a product with ID 1')
     .upon_receiving('a request for a product')
     .with_request('get', '/v2/products/1')
     .will_respond_with(200, body=expected, headers=HeadersFactory()))

    with mock_service:
        # Perform the actual request
        product = client.get_product(1)

        # In this case the mock Provider will have returned a valid response
        assert product.name == expected['name']

        # Make sure that all interactions defined occurred
        mock_service.verify()


def test_get_nonexistent_product(mock_service, client: Client):
    (mock_service
     .given('there is no product with ID 7777')
     .upon_receiving('a request for a product')
     .with_request('get', '/v2/products/7777')
     .will_respond_with(404, body=NotFoundErrorFactory(), headers={
        'Content-Type': 'application/json',
     }))

    with mock_service:
        # Perform the actual request
        status = client.get_product(7777)

        # In this case the mock Provider will have returned a valid response
        assert status is None

        # Make sure that all interactions defined occurred
        mock_service.verify()


def test_delete_nonexistent_product_no_if_match(mock_service, client: Client):
    expected = {
        'code': 428,
        'status': 'Precondition Required',
    }

    (mock_service
     .given('there is no product with ID 7777')
     .upon_receiving('a request to delete a product')
     .with_request('delete', '/v2/products/7777')
     .will_respond_with(428, body=expected, headers={
        'Content-Type': 'application/json',
     }))

    with mock_service:
        # Perform the actual request
        status = client.delete_product(7777)

        # In this case the mock Provider will have returned a valid response
        assert status is False

        # Make sure that all interactions defined occurred
        mock_service.verify()


def test_empty_products_response(mock_service, client: Client):
    headers = HeadersFactory.create()  # type: dict
    headers.update({'X-Pagination': '{"total": 0, "total_pages": 0}'})

    (mock_service
     .given('there are no products')
     .upon_receiving('a request to get list of products')
     .with_request('get', '/v2/products')
     .will_respond_with(200, body=[], headers=headers))

    with mock_service:
        # Perform the actual request
        rv = client.get_products()

        # In this case the mock Provider will have returned a valid response
        assert isinstance(rv, list)
        assert len(rv) == 0

        # Make sure that all interactions defined occurred
        mock_service.verify()


def test_products_response(mock_service, client: Client):
    expected = EachLike(ProductFactory(), minimum=3)
    headers = HeadersFactory.create()  # type: dict
    headers.update({'X-Pagination': json.dumps({
        'total': 3,
        'total_pages': 1,
        'first_page': 1,
        'last_page': 1,
        'page': 1,
    })})

    (mock_service
     .given('there are few products')
     .upon_receiving('a request to get list of products')
     .with_request('get', '/v2/products')
     .will_respond_with(200, body=expected, headers=headers))

    with mock_service:
        # Perform the actual request
        rv = client.get_products()

        # In this case the mock Provider will have returned a valid response
        assert isinstance(rv, list)
        assert len(rv) >= 3
        assert isinstance(rv[0], Product)
        assert isinstance(rv[1], Product)
        assert isinstance(rv[2], Product)

        # Make sure that all interactions defined occurred
        mock_service.verify()


def test_no_products_in_category_response(mock_service, client: Client):
    headers = HeadersFactory.create()  # type: dict
    headers.update({'X-Pagination': '{"total": 0, "total_pages": 0}'})

    (mock_service
     .given('there are no products in category #2')
     .upon_receiving('a request to get list of products')
     .with_request('get', '/v2/products', query={'cid': '2'})
     .will_respond_with(200, body=[], headers=headers))

    with mock_service:
        # Perform the actual request
        rv = client.get_products(params={'cid': 2})

        # In this case the mock Provider will have returned a valid response
        assert isinstance(rv, list)
        assert len(rv) == 0

        # Make sure that all interactions defined occurred
        mock_service.verify()


def test_products_in_category_response(mock_service, client: Client):
    expected = EachLike(ProductFactory(category_id=2), minimum=2)
    headers = HeadersFactory.create()  # type: dict
    headers.update({'X-Pagination': json.dumps({
        'total': 2,
        'total_pages': 1,
        'first_page': 1,
        'last_page': 1,
        'page': 1,
    })})

    (mock_service
     .given('there are few products in category #2')
     .upon_receiving('a request to get list of products')
     .with_request('get', '/v2/products', query={'cid': '2'})
     .will_respond_with(200, body=expected, headers=headers))

    with mock_service:
        # Perform the actual request
        rv = client.get_products(params={'cid': 2})  # type: list[Product]

        # In this case the mock Provider will have returned a valid response
        assert isinstance(rv, list)
        assert len(rv) == 2
        assert isinstance(rv[0], Product)
        assert isinstance(rv[1], Product)
        assert rv[0].category_id == 2
        assert rv[1].category_id == 2

        # Make sure that all interactions defined occurred
        mock_service.verify()


def test_create_product(mock_service, client: Client):
    headers = HeadersFactory.create()  # type: dict
    location = url_term(
        '/v2/products/1',
        'https://example.com/v2/products/1'
    )
    headers.update({'Location': location})

    payload = {
        'description': 'test',
        'discount': 241.93,
        'price': 442.95,
        'rating': 5.0,
        'stock': 123,
        'name': 'test',
        'category_id': 1,
        'brand_id': 1,
    }

    expected = ProductFactory(**payload)

    (mock_service
     .given('there is category #1 and brand #1')
     .upon_receiving('a request to create product')
     .with_request('post', '/v2/products', body=payload, headers={
        'Content-Type': 'application/json'
     })
     .will_respond_with(201, body=expected, headers=headers))

    with mock_service:
        # Perform the actual request
        rv = client.create_product(body=payload)

        # In this case the mock Provider will have returned a valid response
        assert isinstance(rv, Product)
        # assert len(rv) == 0

        # Make sure that all interactions defined occurred
        mock_service.verify()
