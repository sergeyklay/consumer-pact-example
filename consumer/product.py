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


@dataclass(frozen=True)
class Product:
    """Define the basic Product data we expect to receive from the provider."""

    id: int  # pylint: disable=invalid-name
    title: str
    description: str
    price: float
    discount: float
    rating: float
    stock: int
    brand_id: int
    category_id: int


class ProductConsumer:
    """Product Consumer.

    Demonstrate some basic functionality of how the Product Consumer will
    interact with the Product Provider, in this case a simple get_product."""

    def __init__(self, base_uri: str, version: str):
        """Initialise the Consumer, in this case we only need to know the URI.

        :param base_uri: The full URI, including port of the Provider to
                         connect to"""
        self.base_uri = base_uri.rstrip('/')
        self.version = version

    def get_product(self, product_id: int) -> Optional[Product]:
        uri = f'{self.base_uri}/{self.version}/products/{product_id}'
        response = requests.get(uri, timeout=3.0)

        if response.status_code == 404:
            return None
        return Product(**response.json())

    def delete_product(self, product_id: int) -> bool:
        uri = f'{self.base_uri}/{self.version}/products/{product_id}'
        response = requests.delete(uri, timeout=3.0)

        if response.status_code == 204:
            return True
        return False

    def get_products(self, params: dict = None) -> Optional[list]:
        uri = f'{self.base_uri}/{self.version}/products'
        response = requests.get(uri, params=params, timeout=3.0)

        if response.status_code != 200:
            return None

        data = response.json()
        return [Product(**p) for p in data]
