# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Unit tests for consumer utils."""

import pytest

from consumer.utils import intersect_keys, merge_dicts, path


@pytest.mark.parametrize(
    'provided,expected',
    [
        ([{'a': 42}, {'foo': 'bar'}], {'a': 42, 'foo': 'bar'}),
        ([{'a': 42}, {'foo': 'bar', 'a': 17}], {'a': 17, 'foo': 'bar'}),
        ([{'a': 17, 'foo': 'bar'}], {'a': 17, 'foo': 'bar'}),
        ([{'a': 1}, {'b': 2}, {'c': 3}, {'a': 4}], {'a': 4, 'b': 2, 'c': 3}),
    ])
def test_merge(provided, expected):
    assert merge_dicts(*provided) == expected


@pytest.mark.parametrize(
    'search,expected',
    [
        ('a', {'b': {'c': {'d': 42}}}),
        ('a.b', {'c': {'d': 42}}),
        ('a.b.c', {'d': 42}),
        ('a.b.c.d', 42),
        ('a.z.c.d', None),
        ('a.b.c.z', None),
        ('z.y.z', None),
        ('42', None),
    ])
def test_path(search, expected):
    my_dict = {'a': {'b': {'c': {'d': 42}}}}

    if expected is None:
        assert path(my_dict, search) is expected
    else:
        assert path(my_dict, search) == expected


def test_intersect_keys():
    obj = {'include': 'fields', 'foo': 'bar', 'baz': 42}
    keys = {'include', 'limit'}

    expected = {'include': 'fields'}
    assert intersect_keys(obj, keys) == expected

    expected = {'foo': 'bar', 'baz': 42}
    assert intersect_keys(obj, keys, True) == expected
