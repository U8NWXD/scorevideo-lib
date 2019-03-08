# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""Test the :py:class:BaseOps class

"""

from scorevideo_lib.base_utils import BaseOps

# pragma pylint: disable=missing-docstring


class BareClass(BaseOps):

    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.num = 5
        self.lst = ["hi", "A", "?"]

    def add_attribute(self):
        # pylint: disable=attribute-defined-outside-init
        self.letter = "C"


def test_repr():
    test = BareClass()
    test.add_attribute()

    assert repr(test) == "{'num': 5, 'lst': ['hi', 'A', '?'], 'letter': 'C'}"


def test_str():
    test = BareClass()
    test.add_attribute()

    assert repr(test) == str(test)


def test_eq():
    bare1 = BareClass()
    bare2 = BareClass()
    bare2.add_attribute()

    assert bare1 != bare2
    bare1.add_attribute()
    assert bare1 == bare2
