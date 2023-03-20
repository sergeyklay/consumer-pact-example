# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Schemas for handling (de)serialized model representation."""

from marshmallow import fields, post_load, RAISE, Schema

from .models import Brand, Category, Product


class CategorySchema(Schema):
    """Schema for Product Category."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Metaclass to setup CategorySchema."""

        unknown = RAISE

    id = fields.Int(required=True)
    name = fields.Str(required=True)

    @post_load
    def make(self, data, **_kwargs):
        """Deserialize the ``data`` to a Category instance."""
        return Category(**data)


class BrandSchema(Schema):
    """Schema for product brands."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Metaclass to setup BrandSchema."""

        unknown = RAISE

    id = fields.Int(required=True)
    name = fields.Str(required=True)

    @post_load
    def make(self, data, **_kwargs):
        """Deserialize the ``data`` to a Brand instance."""
        return Brand(**data)


class ProductSchema(Schema):
    """Schema for products."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Metaclass to setup ProductSchema."""

        unknown = RAISE
        datetimeformat = '%Y-%m-%dT%H:%M:%S.%f%z'

    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    price = fields.Float(required=True)
    discount = fields.Float(required=True)
    rating = fields.Float(required=True)
    stock = fields.Int(required=True)
    brand_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    updated_at = fields.DateTime(required=True)
    created_at = fields.DateTime(required=True)

    @post_load
    def make(self, data, **_kwargs):
        """Deserialize the ``data`` to a Product instance."""
        return Product(**data)
