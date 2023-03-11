# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Providing various factories for testing purposes."""

import factory
from pact import Format, Like, Term


# Etag header regex.
#
# Examples:
#
#    ETag: "xyzzy"
#    ETag: W/"xyzzy"
#    ETag: ""
#
ETAG_REGEX = r'^(?:\x57\x2f)?"(?:[\x21\x23-\x7e]*|\r\n[\t ]|\.)*"$'


class HeadersFactory(factory.DictFactory):
    class Meta:
        rename = {
            'content_type': 'Content-Type',
            'etag': 'ETag',
        }

    content_type = 'application/json'
    etag = Term(ETAG_REGEX, '"92cfceb39d57d914ed8b14d0e37643de0797ae56"')


class ProductFactory(factory.DictFactory):
    id = Format().integer
    name = Like('Some product name')
    description = Like('Some product description')
    brand_id = Format().integer
    category_id = Format().integer
    price = Format().decimal
    discount = Format().decimal
    rating = Format().decimal
    stock = Format().integer
