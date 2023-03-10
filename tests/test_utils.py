# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Unit tests for consumer utils."""

import pytest

from consumer.utils import merge_dicts


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
