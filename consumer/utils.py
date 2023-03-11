#!/usr/bin/env python
#
# This file is part of the Consumer API example.
#
# Copyright (C) 2023 Serghei Iakovlev <egrep@protonmail.ch>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Various auxiliary utilities for which no dedicated module may be found."""


def merge_dicts(*objects) -> dict:
    """Merge one or more objects into a new object.
    >>> merge({'a': 42}, {'foo': 'bar'})
    {'a': 42, 'foo': 'bar'}
    >>> merge({'a': 42}, {'foo': 'bar', 'a': 17})
    {'a': 17, 'foo': 'bar'}
    >>>  merge({'a': 17, 'foo': 'bar'})
    {'a': 17, 'foo': 'bar'}
    >>> merge({'a': 1}, {'b': 2}, {'c': 3}, {'a': 4})
    {'a': 4, 'b': 2, 'c': 3}
    """
    result = {}
    for obj in objects:
        result.update(obj)

    return result
