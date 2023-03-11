# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Providing various factories for testing purposes."""

import factory
from pact import Format, Like, Term

# RegExp to test a string for a full ISO 8601 Date.
# Does not do any sort of date validation, only checks if the string is
# according to the ISO 8601 spec.
#
# Examples:
#
#    2016-12-15T20:16:01
#    2023-12-15T20:16:01Z
#    2010-05-01T01:14:31.876
#    2016-05-24T15:54:14.00000Z
#    1994-11-05T08:15:30-05:00
#    2002-01-31T23:00:00.1234-02:00
#
ISO_8601_REGEX = r'^\d{4}-[01]\d-[0-3]\d\x54[0-2]\d:[0-6]\d:[0-6]\d(?:\.\d+)?(?:(?:[+-]\d\d:\d\d)|\x5A)?$'  # noqa: E501

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
    created_at = Term(ISO_8601_REGEX, '2002-12-31T23:00:00+01:00')
    updated_at = Term(ISO_8601_REGEX, '2016-12-15T20:16:01Z')
