# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Providing various factories for testing purposes."""

import factory
from pact import Format, Like, Term


def url_term(path: str, generate: str):
    """Create URL pattern for matching with server response.

    For demonstration purposes, it can be moderately simple and not
    cover all possibilities."""
    return Term(
        r'https?://[-a-zA-Z0-9@:%._\+~#=]{1,256}' + path,
        generate)


class HeadersFactory(factory.DictFactory):
    class Meta:
        rename = {
            'content_type': 'Content-Type',
            'etag': 'ETag',
        }

    content_type = 'application/json'
    etag = Term(
        '(?:W/)?"(?:[ !#-\x7E\x80-\xFF]*|\r\n[\t ]|\\.)*"',
        '"92cfceb39d57d914ed8b14d0e37643de0797ae56"',
    )


class ProductFactory(factory.DictFactory):
    id = Format().integer
    title = Like('Some product title')
    description = Like('Some product description')
    brand_id = Format().integer
    category_id = Format().integer
    price = Format().decimal
    discount = Format().decimal
    rating = Format().decimal
    stock = Format().integer
