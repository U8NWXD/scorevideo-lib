# This file is part of scorevideo_lib: A library for working with scorevideo
# Copyright (C) 2018  U8N WXD <cs.temporary@icloud.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Callable, Iterable, List, Any

"""Basic utilities for generally applicable functions

"""


class BaseOps:
    """Superclass for basic operations

    """

    def __repr__(self):
        # pylint: disable=missing-docstring
        return str(self.__dict__)

    def __str__(self):
        # pylint: disable=missing-docstring
        return self.__repr__()

    def __eq__(self, other):
        # pylint: disable=missing-docstring
        return self.__repr__() == other.__repr__()


def add_to_partition(elem: object, partitions: List[List[object]],
                     is_equiv: Callable[[object, object], bool]):
    """Helper function to add an element to an appropriate equivalence class

    Adds the element to an existing class if one is available or creates a
    new class by adding a partition if necessary.

    Args:
        elem: The element to add
        partitions: The list of equivalence classes to add ``elem`` to
        is_equiv: A function that accepts two elements of lst and returns
            whether those elements should be in the same equivalence class.
            For proper functioning, should implement an equivalence relation.

    Returns: The equivalence classes provided but with ``elem`` added.

    """
    for partition in partitions:
        if is_equiv(elem, partition[0]):
            partition.append(elem)
            return
    partitions.append([elem])
    return partitions


def equiv_partition(lst: Iterable[object],
                    is_equiv: Callable[[object, object], bool]):
    """Splits elements into equivalence classes using a provided callback

    Args:
        lst: The elements to divide in to equivalence classes. Is not modified.
        is_equiv: A function that accepts two elements of lst and returns
            whether those elements should be in the same equivalence class.
            For proper functioning, should implement an equivalence relation.

    Returns: A list of the partitions. Each element will be in exactly one
        partition.

    """
    partitions = []
    for elem in lst:
        add_to_partition(elem, partitions, is_equiv)
    return partitions


def remove_trailing_newline(s: str):
    if len(s) > 0 and s[-1] == "\n":
        s = s[:-1]
    return s
