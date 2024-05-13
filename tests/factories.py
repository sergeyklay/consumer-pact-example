# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Providing various factories for testing purposes."""

import datetime
import hashlib
from enum import Enum

import factory
from pact import Format as BaseFormat, Like, Term


class Format(BaseFormat):
    """Class of regular expressions for common formats."""

    def __init__(self):
        super().__init__()

        self.etag = self.etag()
        self.last_modified = self.last_modified()
        self.media_type_json = self.media_type_json()

    def url(self, path: str, generate: str):
        """Match and URL.

         For demonstration purposes, it can be moderately simple and not
         cover all possibilities."""
        return Term(
            fr'^https?://[-a-zA-Z0-9@:%._\+~#=]{{1,256}}{path}$',
            generate
        )

    def last_modified(self):
        """Match date and time format used in the Last-Modified header.

        Matches the date and time format according to RFC 7231 is described in
        section 7.1.1.1. Examples of matched dates are:

        * Mon, 12 Feb 2022 11:36:28 GMT
        * Sat, 11 Mar 2023 21:56:41 GMT
        """
        return Term(
            self.RegexesEx.last_modified.value,
            'Mon, 12 Feb 2022 11:36:28 GMT'
        )

    def etag(self):
        """Match a string for used in the Etag header.

        Matches the following headers:

        * ETag: "abee653e458eb31e7d21ebff89f79232b482c885"
        * ETag: W/"abee653e458eb31e7d21ebff89f79232b482c885"
        * ETag: ""
        """
        return Term(
            self.RegexesEx.etag.value,
            f'''"{hashlib.sha1(bytes('{}', 'utf-8')).hexdigest()}"'''
        )

    def media_type_json(self):
        """Match json media type used in the Content-Type header.

        Matches the following media types:

        * application/json
        * application/json; charset=utf-8
        """
        return Term(
            self.RegexesEx.media_type_json.value,
            'application/json; charset=utf-8'
        )

    class RegexesEx(Enum):
        """Regex Enum for common formats."""

        last_modified = r'^[A-Za-z]{3},\s\d{2}\s[A-Za-z]{3}\s\d{4}\s\d{2}:' \
                        r'\d{2}:\d{2}\sGMT$'
        etag = r'^(?:\x57\x2f)?"(?:[\x21\x23-\x7e]*|\r\n[\t ]|\.)*"$'
        media_type_json = r'^application/json(;\s?charset=[\w-]+)?$'


class NotFoundErrorFactory(factory.DictFactory):
    message = 'Product not found'
    code = 404
    status = 'Not Found'


class HeadersFactory(factory.DictFactory):
    class Meta:
        rename = {
            'content_type': 'Content-Type',
            'etag': 'ETag',
        }

    content_type = Format().media_type_json
    etag = Format().etag


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
    created_at = BaseFormat().iso_datetime_ms
    updated_at = BaseFormat().iso_datetime_ms
