# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Pact test for Product service client."""

import atexit
import logging

import pytest
from pact import Consumer, EachLike, Provider, Term

from consumer.product import Product
from .factories import (
    HeadersFactory,
    LinksFactory,
    PaginationFactory,
    ProductFactory,
    url_term
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def pact(mock_opts, pact_dir, app_version):
    """Set up a Pact Consumer, which provides the Provider mock service."""
    consumer = Consumer('ProductServiceClient', version=app_version)
    pact = consumer.has_pact_with(
        Provider('ProductService'),
        pact_dir=pact_dir,
        **mock_opts,
    )

    pact.start_service()

    # Make sure the Pact mocked provider is stopped when we finish, otherwise
    # port 1234 may become blocked
    atexit.register(pact.stop_service)

    yield pact

    # This will stop the Pact mock server, and if publish is True, submit Pacts
    # to the Pact Broker
    pact.stop_service()

    # Given we have cleanly stopped the service, we do not want to re-submit
    # the Pacts to the Pact Broker again atexit, since the Broker may no longer
    # be available if it has been started using the --run-broker option, as it
    # will have been torn down at that point
    pact.publish_to_broker = False


def test_get_existent_product(pact, consumer):
    # Define the Matcher; the expected structure and content of the response
    expected = ProductFactory(title='product0')

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a body which is
    # "Like" the structure defined above. This means the mock provider will
    # return the EXACT content where defined, e.g. 'product0' for title, and
    # SOME appropriate content e.g. for description.
    (pact
     .given('there is a product with ID 1')
     .upon_receiving('a request for a product')
     .with_request('get', '/v1/products/1')
     .will_respond_with(200, body=expected, headers=HeadersFactory()))

    with pact:
        # Perform the actual request
        product = consumer.get_product(1)

        # In this case the mock Provider will have returned a valid response
        assert product.title == expected['title']

        # Make sure that all interactions defined occurred
        pact.verify()


def test_get_nonexistent_product(pact, consumer):
    expected = {
        'description': Term(r'Invalid resource URI.', 'Invalid resource URI.'),
        'status': 404,
        'title': Term(r'Not Found', 'Not Found'),
    }

    (pact
     .given('there is no product with ID 7777')
     .upon_receiving('a request for a product')
     .with_request('get', '/v1/products/7777')
     .will_respond_with(404, body=expected, headers={
        'Content-Type': 'application/json',
     }))

    with pact:
        # Perform the actual request
        status = consumer.get_product(7777)

        # In this case the mock Provider will have returned a valid response
        assert status is None

        # Make sure that all interactions defined occurred
        pact.verify()


def test_delete_nonexistent_product(pact, consumer):
    expected = {
        'description': Term(r'Invalid resource URI.', 'Invalid resource URI.'),
        'status': 404,
        'title': Term(r'Not Found', 'Not Found'),
    }

    (pact
     .given('there is no product with ID 7777')
     .upon_receiving('a request to delete a product')
     .with_request('delete', '/v1/products/7777')
     .will_respond_with(404, body=expected, headers={
        'Content-Type': 'application/json',
     }))

    with pact:
        # Perform the actual request
        status = consumer.delete_product(7777)

        # In this case the mock Provider will have returned a valid response
        assert status is False

        # Make sure that all interactions defined occurred
        pact.verify()


def test_empty_products_response(pact, consumer):
    first = url_term(
        r'/v1/products\?page=1&per_page=10',
        'https://example.com/v1/products?page=1&per_page=10'
    )
    self = url_term('/v1/products', 'https://example.com/v1/products')
    expected = {
        'links': LinksFactory(first=first, last=first, self=self),
        'pagination': PaginationFactory(total=0),
        'products': [],
    }

    (pact
     .given('there are no products')
     .upon_receiving('a request to get list of products')
     .with_request('get', '/v1/products')
     .will_respond_with(200, body=expected, headers=HeadersFactory()))

    with pact:
        # Perform the actual request
        rv = consumer.get_products()

        # In this case the mock Provider will have returned a valid response
        assert isinstance(rv, dict)
        assert isinstance(rv['links'], dict)
        assert isinstance(rv['pagination'], dict)
        assert isinstance(rv['products'], list)
        assert len(rv['products']) == 0

        # Make sure that all interactions defined occurred
        pact.verify()


def test_expanded_products_response(pact, consumer):
    first = url_term(
        r'/v1/products\?page=1&per_page=10&expanded=1',
        'https://example.com/v1/products?page=1&per_page=10&expanded=1'
    )
    self = url_term(
        r'/v1/products\?expanded=1',
        'https://example.com/v1/products?expanded=1',
    )

    expected = {
        'links': LinksFactory(first=first, last=first, self=self),
        'pagination': PaginationFactory(),
        'products': EachLike(ProductFactory(), minimum=3)}

    (pact
     .given('there are few products')
     .upon_receiving('a request to get expanded list of products')
     .with_request('get', '/v1/products', query={'expanded': '1'})
     .will_respond_with(200, body=expected, headers=HeadersFactory()))

    with pact:
        # Perform the actual request
        rv = consumer.get_products(params={'expanded': 1})

        # In this case the mock Provider will have returned a valid response
        assert isinstance(rv, dict)
        assert isinstance(rv['links'], dict)
        assert isinstance(rv['pagination'], dict)
        assert isinstance(rv['products'], list)
        assert len(rv['products']) > 1
        assert isinstance(rv['products'][0], Product)
        assert isinstance(rv['products'][1], Product)

        # Make sure that all interactions defined occurred
        pact.verify()


def test_collapsed_products_response(pact, consumer):
    first = url_term(
        r'/v1/products\?page=1&per_page=10',
        'https://abc.cde/v1/products?page=1&per_page=10'
    )
    self = url_term(
        r'/v1/products\?expanded=0',
        'https://abc.cde/v1/products?expanded=0',
    )
    expected_body = {
        'links': LinksFactory(first=first, last=first, self=self),
        'pagination': PaginationFactory(),
        'products': EachLike(
            url_term('/v1/products/[0-9]+', 'https://abc.cde/v1/products/1'),
            minimum=3
        )
    }

    (pact
     .given('there are few products')
     .upon_receiving('a request to get collapsed list of products')
     .with_request('get', '/v1/products', query={'expanded': '0'})
     .will_respond_with(200, body=expected_body, headers=HeadersFactory()))

    with pact:
        # Perform the actual request
        rv = consumer.get_products(params={'expanded': 0})

        # In this case the mock Provider will have returned a valid response
        assert isinstance(rv, dict)
        assert isinstance(rv['links'], dict)
        assert isinstance(rv['pagination'], dict)
        assert isinstance(rv['products'], list)
        assert len(rv['products']) > 1
        assert isinstance(rv['products'][0], str)
        assert isinstance(rv['products'][1], str)

        # Make sure that all interactions defined occurred
        pact.verify()
