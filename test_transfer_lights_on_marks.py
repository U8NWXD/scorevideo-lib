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

import os
from shutil import copytree, rmtree
from transfer_lights_on_marks import batch_mark_lights_on

TEST_RES = "tests/res"

# pragma pylint: disable=missing-docstring


def test_batch_mark_lights_on():
    src = os.path.join(TEST_RES, "lightsOn")
    dst = os.path.join(TEST_RES, "tmp")
    copytree(src, dst)
    try:
        batch_mark_lights_on(dst)
        scored_name = "log050118_OD1030618_TA23_Dyad_Morning.avi_CS.txt"
        expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
        with open(os.path.join(dst, scored_name)) as actual_file:
            with open(os.path.join(src, scored_name)) as expected_file:
                actual = actual_file.readlines()
                expected = expected_file.readlines()
                expected.insert(len(expected) - 1, expected_mark)
        rmtree(dst)
    except Exception as e:
        rmtree(dst)
        raise e
    for line in actual:
        print(line, end="")
    assert actual == expected

# TODO: More thorough testing
