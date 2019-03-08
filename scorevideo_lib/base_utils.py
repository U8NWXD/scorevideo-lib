# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""Basic utilities for generally applicable functions

"""

from typing import Callable, Iterable, List


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


def add_to_partition(elem: str, partitions: List[List[str]],
                     is_equiv: Callable[[str, str], bool]):
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
            return partitions
    partitions.append([elem])
    return partitions


def equiv_partition(lst: Iterable[str],
                    is_equiv: Callable[[str, str], bool]) \
        -> List[List[str]]:
    """Splits elements into equivalence classes using a provided callback

    Args:
        lst: The elements to divide in to equivalence classes. Is not modified.
        is_equiv: A function that accepts two elements of lst and returns
            whether those elements should be in the same equivalence class.
            For proper functioning, should implement an equivalence relation.

    Returns: A list of the partitions. Each element will be in exactly one
        partition.

    """
    partitions = []  # type: List[List[str]]
    for elem in lst:
        add_to_partition(elem, partitions, is_equiv)
    return partitions


def remove_trailing_newline(s: str):
    r"""Remove a single trailing newline if it exists in a string

    >>> remove_trailing_newline('s\n')
    's'
    >>> remove_trailing_newline('s')
    's'
    >>> remove_trailing_newline('s\n\n')
    's\n'

    Args:
        s: The string to remove a newline from

    Returns: ``s``, but without a terminal trailing newline, if it was present

    """
    # For how to include `\n` in doctests: https://stackoverflow.com/a/8849771
    if s and s[-1] == "\n":
        s = s[:-1]
    return s
