#!/usr/bin/env python
#
# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from dataclasses import dataclass
from typing import Optional

import requests

from consumer.utils import merge_dicts


@dataclass(frozen=True)
class Product:
    """Define the basic Product data we expect to receive from the provider."""

    id: int  # pylint: disable=invalid-name
    name: str
    description: str
    price: float
    discount: float
    rating: float
    stock: int
    brand_id: int
    category_id: int
    created_at: str
    updated_at: str


class Client:
    """Product Consumer.

    Demonstrate some basic functionality of how the Product Consumer will
    interact with the Product Provider, in this case a simple get_product."""

    DEFAULT_OPTIONS = {
        # API endpoint base URL to connect to.
        'base_url': 'http://localhost',

        # Used API version.
        'version': 'v1',
    }

    def __init__(self, **options):
        """A :class:`Client` object for interacting with API."""
        self.options = merge_dicts(self.DEFAULT_OPTIONS, options)
        self.headers = options.pop('headers', {})

    def get_product(self, product_id: int) -> Optional[Product]:
        url = (f"{self.options['base_url'].rstrip('/')}"
               f"/{self.options['version']}"
               f"/products/{product_id}")

        response = requests.get(url, timeout=3.0)
        if response.status_code == 404:
            return None

        return Product(**response.json())

    def delete_product(self, product_id: int) -> bool:
        url = (f"{self.options['base_url'].rstrip('/')}"
               f"/{self.options['version']}"
               f"/products/{product_id}")

        response = requests.delete(url, timeout=3.0)
        if response.status_code == 204:
            return True

        return False

    def get_products(self, params: dict = None) -> Optional[list]:
        url = (f"{self.options['base_url'].rstrip('/')}"
               f"/{self.options['version']}"
               f"/products")

        response = requests.get(url, params=params, timeout=3.0)
        if response.status_code != 200:
            return None

        return [Product(**p) for p in response.json()]
