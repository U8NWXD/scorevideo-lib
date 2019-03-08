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
from pytest import fixture
from scorevideo_lib.transfer_lights_on_marks import batch_mark_lights_on

TEST_RES = "tests/res"

# pragma pylint: disable=missing-docstring


@fixture
def temp_test_dir():
    src = os.path.join(TEST_RES, "lightsOn")
    dst = os.path.join(TEST_RES, "tmp")
    copytree(src, dst)
    yield src, dst
    rmtree(dst)


def lights_on_test_helper(temp_test_dir, scored_name, expected_mark):
    src, dst = temp_test_dir
    batch_mark_lights_on(dst)
    with open(os.path.join(dst, scored_name)) as actual_file:
        with open(os.path.join(src, scored_name)) as expected_file:
            actual = actual_file.readlines()
            expected = expected_file.readlines()
            expected.insert(len(expected) - 1, expected_mark)
    assert actual == expected


def test_mark_lights_on(temp_test_dir):
    scored_name = "log050118_OD1030618_TA23_Dyad_Morning.avi_CS.txt"
    expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
    lights_on_test_helper(temp_test_dir, scored_name, expected_mark)


def test_mark_lights_on_no_behav_1st(temp_test_dir):
    scored_name = "log120118_OD1030618_OC4A_Dyad_Morning.avi_CS.txt"
    expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
    lights_on_test_helper(temp_test_dir, scored_name, expected_mark)


def test_mark_lights_on_no_behav_scored(temp_test_dir):
    scored_name = "log120118_OD1100618_OC4A_Dyad_Morning.avi_CS.txt"
    expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
    lights_on_test_helper(temp_test_dir, scored_name, expected_mark)


def test_mark_lights_on_empty_1st_neg_behav(temp_test_dir):
    scored_name = "log050118_OB5B030618_TA23_Dyad_Morning.avi_CS.txt"
    expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
    lights_on_test_helper(temp_test_dir, scored_name, expected_mark)
