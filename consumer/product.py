#!/usr/bin/env python
#
# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from typing import Optional

import requests


class Product:
    """Define the basic Product data we expect to receive from the provider."""

    def __init__(self, title: str, description: str, price: float):
        self.title = title
        self.description = description
        self.price = price

    def __repr__(self):
        """Returns the object representation in string format."""
        return f'<Product {self.title}>'


class ProductConsumer:
    """Product Consumer.

    Demonstrate some basic functionality of how the Product Consumer will
    interact with the Product Provider, in this case a simple get_product."""

    API_VERSION = 'v1'

    def __init__(self, base_uri: str):
        """Initialise the Consumer, in this case we only need to know the URI.

        :param base_uri: The full URI, including port of the Provider to
                         connect to"""
        self.base_uri = base_uri.rstrip('/')

    def get_product(self, product_id: int) -> Optional[Product]:
        uri = f'{self.base_uri}/{self.API_VERSION}/products/{product_id}'
        response = requests.get(uri, timeout=3.0)

        if response.status_code == 404:
            return None

        data = response.json()

        return Product(
            title=data['title'],
            description=data['description'],
            price=data['price'],
        )

    def delete_product(self, product_id: int) -> bool:
        uri = f'{self.base_uri}/{self.API_VERSION}/products/{product_id}'
        response = requests.delete(uri, timeout=3.0)

        if response.status_code == 204:
            return True
        return False

    def get_products(self, params: dict = None) -> Optional[dict]:
        uri = f'{self.base_uri}/{self.API_VERSION}/products'
        response = requests.get(uri, params=params, timeout=3.0)

        if response.status_code != 200:
            return None

        data = response.json()
        rv = {
            'links': data['links'],
            'pagination': data['pagination'],
            'products': [],
        }

        for p in data['products']:
            if params and 'expanded' in params and params['expanded'] == 0:
                rv['products'].append(p)
            else:
                rv['products'].append(
                    Product(
                        title=p['title'],
                        description=p['description'],
                        price=p['price'],
                    )
                )

        return rv
