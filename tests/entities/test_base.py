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

import pickle

import pytest

from consumer.entities.base import BaseEntity


class MyEntity(BaseEntity):
    pass


def test_to_dict():
    entity = MyEntity(1)
    assert entity.to_dict() == {'id': 1}

    entity.attributes.update({'name': 'foo'})
    assert entity.to_dict() == {
        'id': 1,
        'name': 'foo',
    }


def test_set_state():
    state = {
        'id': 42,
        'name': 'my_entity',
        'description': 'some entity',
    }

    entity = MyEntity(8)
    entity.__setstate__(state)

    assert entity.id == 42
    assert entity.attributes == {
        'id': 42,
        'name': 'my_entity',
        'description': 'some entity',
    }


def test_get_state():
    entity = MyEntity(117)
    entity.attributes.update({'abc': 'def'})

    serialized = pickle.dumps(entity)
    deserialized = pickle.loads(serialized)

    assert deserialized.id == 117
    assert deserialized.abc == 'def'


def test_get_invalid_attr():
    entity = MyEntity(1)
    with pytest.raises(AttributeError) as exc_info:
        _ = entity.abc

    assert "'MyEntity' object has no attribute 'abc'" in str(exc_info.value)


def test_get_set_attr():
    entity = MyEntity(1)

    assert entity.id == 1
    assert entity['id'] == 1

    assert 'abc' not in entity
    entity.abc = 42

    assert entity.abc == 42
    assert entity['abc'] == 42
    assert 'abc' in entity
