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

"""Unit tests for the :py:class:Mark class

"""

import pytest
from scorevideo_lib.parse_log import Mark

# pragma pylint: disable=missing-docstring


def test_init_valid_start():
    Mark("    1     0:00.03    video start")


def test_init_valid_end():
    Mark("54001    30:00.03    video end")


def test_init_invalid_two_spaces_in_name():
    with pytest.raises(TypeError):
        Mark("    1     0:00.03    video  start")


def test_init_invalid_one_space_after_time():
    with pytest.raises(TypeError):
        Mark("    1     0:00.03 video start")


def test_init_invalid_one_space_after_frame():
    with pytest.raises(TypeError):
        Mark("    1 0:00.03    video start")


def test_init_invalid_time_no_period():
    with pytest.raises(TypeError):
        Mark("    1     0:00:03    video start")


def test_init_invalid_time_two_periods():
    with pytest.raises(TypeError):
        Mark("    1     0.00.03    video start")


def test_init_invalid_time_one_middle_digit():
    with pytest.raises(TypeError):
        Mark("    1     0:0.03    video start")


def test_init_invalid_time_negative():
    with pytest.raises(TypeError):
        Mark("    1     -0:00.03    video start")


def test_init_invalid_negative_frame():
    with pytest.raises(TypeError):
        Mark("    -1     0:00.03    video start")


def test_init_invalid_name():
    with pytest.raises(TypeError):
        Mark("    1     0:00.03    video start!")


def test_init_valid_long_time():
    Mark("    1     01:20:04.03    video start")
