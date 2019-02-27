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

# TODO: Use hypothesis here
