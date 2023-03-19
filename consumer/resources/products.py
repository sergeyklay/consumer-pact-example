# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Products API resource module."""

from consumer.entities.products import Product as ProductEntity
from . import BaseResource


class Products(BaseResource):
    """Represent Products API resource."""

    def get(self, product_id: int) -> ProductEntity:
        """Get the requested product."""
        url = self.resolve_endpoint(f'products/{product_id}')
        rv, _ = self.client.get(url)

        return ProductEntity.from_dict(rv)

    def delete(self, product_id: int, **options) -> bool:
        """Get the requested product."""
        url = self.resolve_endpoint(f'products/{product_id}')
        _, _ = self.client.delete(url, **options)

        return True

    def create(self, **data) -> ProductEntity:
        """Create a product."""
        url = self.resolve_endpoint('products')
        rv, _ = self.client.post(url, data=data)

        return ProductEntity.from_dict(rv)

    def all(self, **options) -> list[ProductEntity]:
        """Get list of products."""
        url = self.resolve_endpoint('products')
        rv, _ = self.client.get(url, **options)

        return ProductEntity.from_collection(rv)
