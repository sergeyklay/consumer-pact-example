# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Products API resource module."""

from consumer.models import Product
from consumer.schemas import ProductSchema
from . import BaseResource


class Products(BaseResource):
    """Represent Products API resource."""

    def get(self, product_id: int) -> Product:
        """Get the requested product."""
        url = self.resolve_endpoint(f'products/{product_id}')
        response = self.client.get(url)

        schema = ProductSchema()
        return schema.load(response.json())

    def delete(self, product_id: int, **options) -> bool:
        """Get the requested product."""
        url = self.resolve_endpoint(f'products/{product_id}')
        response = self.client.delete(url, **options)

        return response.status_code == 204

    def create(self, **data) -> Product:
        """Create a product."""
        url = self.resolve_endpoint('products')
        response = self.client.post(url, data=data)

        schema = ProductSchema()
        return schema.load(response.json())

    def all(self, **options) -> list[Product]:
        """Get list of products."""
        url = self.resolve_endpoint('products')
        response = self.client.get(url, **options)

        schema = ProductSchema()
        return [schema.load(p) for p in response.json()]
