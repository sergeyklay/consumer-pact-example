# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Module providing the functionality of data models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Category:
    """Define the Category model we expect to receive from the provider."""

    id: int  # pylint: disable=invalid-name
    name: str

    def __repr__(self):
        """Provide an easy-to-read description of the current instance."""
        return f'<{self.__class__.__name__}: id={self.id}>'


@dataclass(frozen=True)
class Brand:
    """Define the Brand model data we expect to receive from the provider."""

    id: int  # pylint: disable=invalid-name
    name: str

    def __repr__(self):
        """Provide an easy-to-read description of the current instance."""
        return f'<{self.__class__.__name__}: id={self.id}>'


@dataclass(frozen=True)
class Product:  # pylint: disable=too-many-instance-attributes
    """Define the Product model data we expect to receive from the provider."""

    id: int  # pylint: disable=invalid-name
    name: str
    description: str
    price: float
    discount: float
    rating: float
    stock: int
    brand_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime

    def __repr__(self):
        """Provide an easy-to-read description of the current instance."""
        return f'<{self.__class__.__name__}: id={self.id}>'
