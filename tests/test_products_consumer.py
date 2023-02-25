# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Pact test for Product service client"""

import logging

from pact import Like, Format

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def test_get_product(pact, consumer):
    # Define the Matcher; the expected structure and content of the response
    expected = {
        'id': Format().integer,
        'title': 'Over group reach plan health',
        'description': Like('Chair answer nature do benefit be tonight make travel season itself weight hard.'),
        'brand': Like('Wilson Inc'),
        'category': Like('around'),
        'price': Format().decimal,
        'discount': Format().decimal,
        'rating': Format().decimal,
        'stock': Format().integer,
    }

    # Define the expected behaviour of the Provider. This determines how the
    # Pact mock provider will behave. In this case, we expect a body which is
    # "Like" the structure defined above. This means the mock provider will
    # return the EXACT content where defined, e.g. Product_X for title, and
    # SOME appropriate content e.g. for description.
    (pact
     .given('there is a product with ID 1')
     .upon_receiving('a request for a product')
     .with_request('get', '/v1/products/1')
     .will_respond_with(200, body=Like(expected)))

    with pact:
        # Perform the actual request
        product = consumer.get_product(1)

        # In this case the mock Provider will have returned a valid response
        assert product.title == expected['title']

        # Make sure that all interactions defined occurred
        pact.verify()
