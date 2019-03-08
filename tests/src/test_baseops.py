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
