# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The top-level module for consumer resources.

This module provides base resource class used by various resource
classes within Consumer API example.
"""

from abc import ABCMeta


# pylint: disable=too-few-public-methods
class BaseResource(metaclass=ABCMeta):
    """Base resource class."""

    API_VERSION = 'v2'

    def __init__(self, client, api_version=None):
        """A :class:`BaseResource` base object for consumer resources."""
        self.client = client
        self.api_version = api_version or BaseResource.API_VERSION

    def resolve_endpoint(self, path: str) -> str:
        """Resolve resource endpoint taking into account API version.

        >>> self.resolve_endpoint('/products')
        /v1/products
        >>> self.resolve_endpoint('products/42')
        /v1/products/42
        """
        return f"/{self.api_version.strip('/')}/{path.lstrip('/')}"