# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Providing various factories for testing purposes."""

import factory
from pact import Term


def url_term(path: str, generate: str):
    """Create URL pattern for matching with server response.

    For demonstration purposes, it can be moderately simple and not
    cover all possibilities."""
    return Term(
        r'https?://[-a-zA-Z0-9@:%._\+~#=]{1,256}' + path,
        generate)


class PaginationFactory(factory.DictFactory):
    page = 1
    pages = 1
    per_page = 10
    total = 3


class LinksFactory(factory.DictFactory):
    first = None
    last = None
    next = None
    prev = None
    self = None
