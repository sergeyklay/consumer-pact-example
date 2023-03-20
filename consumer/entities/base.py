# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The base module for consumer entities.

This module provides base entity class used by various entities
classes within Consumer API example.
"""

from abc import ABCMeta


class BaseEntity(metaclass=ABCMeta):
    """Base entity class."""

    def __init__(self, entity_id):
        """Initialize current entity."""
        self.attributes = {'id': entity_id}

    def __getattr__(self, item):
        """Invoke for any attr not in the instance's __dict__."""
        if item in super().__getattribute__('attributes'):
            return super().__getattribute__('attributes')[item]

        msg = f"'{self.__class__.__name__}' object has no attribute '{item}'"
        raise AttributeError(msg)

    def __setattr__(self, key, value):
        """Implement setattr(self, name, value)."""
        internal = ('attributes', )
        if key in internal:
            return super().__setattr__(key, value)
        return super().__getattribute__('attributes').update({key: value})

    def __getitem__(self, item):
        """Getter for the attribute value."""
        return self.attributes[item]

    def __setitem__(self, key, value):
        """Setter for the attribute value."""
        self.attributes[key] = value

    def __contains__(self, item):
        """Attribute membership verification."""
        return item in self.attributes

    def __repr__(self):
        """Provide an easy-to-read description of the current entity."""
        return f'<{self.__class__.__name__}: id={self.id}>'

    def __setstate__(self, data: dict):
        """Play nice with pickle."""
        self.attributes = {}
        for key, val in data.items():
            self.attributes[key] = val

    def __getstate__(self):
        """Play nice with pickle."""
        return self.to_dict()

    def to_dict(self):
        """Convert this entity to a dictionary."""
        return self.attributes

    @classmethod
    def from_dict(cls, fields):
        """Create an instance of the current class from the provided data."""
        entity = cls(entity_id=None)
        entity.__setstate__(fields)

        return entity

    @classmethod
    def from_collection(cls, data: list) -> list:
        """
        Create a list of instances of the current class from the provided data.
        """
        entities = []
        for fields in data:
            entity = cls(entity_id=None).from_dict(fields)
            entities.append(entity)

        return entities
