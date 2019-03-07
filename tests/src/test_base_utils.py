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

"""Test the utilities in :py:mod:`scorevideo_lib.base_utils`

"""
from hypothesis import given, example
from hypothesis.strategies import text, lists
from scorevideo_lib.base_utils import equiv_partition

TEST_RES = "tests/res"

# pragma pylint: disable=missing-docstring


def test_equiv_partition_simple():
    nums = [1, 1, 5, 6, 3, 8, 8, 5, 7, 3, 5, 4, 7, 8]
    nums_orig = nums.copy()
    partitions = equiv_partition(nums, lambda x, y: x == y)
    exp = [[1, 1], [5, 5, 5], [6], [3, 3], [8, 8, 8], [7, 7], [4]]
    assert partitions == exp
    assert nums == nums_orig


def str_equiv(x, y):
    if not x or not y:
        return not x and not y
    return x[0] == y[0]


# For how to get lists of strings: https://stackoverflow.com/q/43282267
@given(lists(text()))
@example(['', '0', '/'])
def test_equiv_partition_text(lst):
    orig = lst.copy()
    partitions = equiv_partition(lst, str_equiv)

    # Check that elements of a given partition are equivalent
    for part in partitions:
        for x in part:
            for y in part:
                assert str_equiv(x, y)

    # Check that elements of distinct partitions are not equivalent
    for p_1 in partitions:
        for p_2 in partitions:
            if p_1 != p_2:
                for x in p_1:
                    for y in p_2:
                        assert not str_equiv(x, y)

    # Check that equiv_partition doesn't modify the list
    assert orig == lst
