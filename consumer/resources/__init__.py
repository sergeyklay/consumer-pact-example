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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from consumer.client import Client


# pylint: disable=too-few-public-methods
class BaseResource(metaclass=ABCMeta):
    """Base resource class."""

    API_VERSION = 'v2'

    def __init__(self, client: 'Client', api_version=None):
        """A :class:`BaseResource` base object for consumer resources."""
        self.client = client
        self.api_version = api_version or BaseResource.API_VERSION

    def resolve_endpoint(self, path: str) -> str:
        """Resolve resource endpoint taking into account API version.

        >>> from consumer.client import Client
        >>> resource = BaseResource(Client())
        >>> resource.resolve_endpoint('/products')
        '/v2/products'
        >>> resource.resolve_endpoint('products/42')
        '/v2/products/42'
        >>> resource.api_version = 'v1'
        >>> resource.resolve_endpoint('/products')
        '/v1/products'
        """
        return f"/{self.api_version.strip('/')}/{path.lstrip('/')}"
