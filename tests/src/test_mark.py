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

from datetime import timedelta
import pytest
from scorevideo_lib.parse_log import Mark

# pragma pylint: disable=missing-docstring


def test_from_line_valid_start():
    mark = Mark.from_line("    1     0:00.03    video start")
    assert mark.frame == 1
    assert mark.time == timedelta(seconds=0.03)
    assert mark.name == "video start"


def test_from_line_valid_end():
    mark = Mark.from_line("54001    30:00.03    video end")
    assert mark.frame == 54001
    assert mark.time == timedelta(seconds=1800.03)
    assert mark.name == "video end"


def test_from_line_invalid_two_spaces_in_name():
    with pytest.raises(TypeError):
        Mark.from_line("    1     0:00.03    video  start")


def test_from_line_invalid_one_space_after_time():
    with pytest.raises(TypeError):
        Mark.from_line("    1     0:00.03 video start")


def test_from_line_invalid_one_space_after_frame():
    with pytest.raises(TypeError):
        Mark.from_line("    1 0:00.03    video start")


def test_from_line_invalid_time_no_period():
    with pytest.raises(TypeError):
        Mark.from_line("    1     0:00:03    video start")


def test_from_line_invalid_time_two_periods():
    with pytest.raises(TypeError):
        Mark.from_line("    1     0.00.03    video start")


def test_from_line_invalid_time_one_middle_digit():
    with pytest.raises(TypeError):
        Mark.from_line("    1     0:0.03    video start")


def test_from_line_valid_negative_frame():
    Mark.from_line("    -1     0:00.03    video start")


def test_from_line_valid_time_negative():
    Mark.from_line("    1     -0:00.03    video start")


def test_from_line_invalid_frame_nonnumeric():
    with pytest.raises(TypeError):
        Mark.from_line("    a1     0:00.03    video start")


def test_from_line_invalid_time_nonnumeric():
    with pytest.raises(TypeError):
        Mark.from_line("    1     0:a00.03    video start")


def test_from_line_invalid_name():
    with pytest.raises(TypeError):
        Mark.from_line("    1     0:00.03    video start!")


def test_from_line_valid_long_time():
    mark = Mark.from_line("    1     01:20:04.03    video start")
    assert mark.frame == 1
    assert mark.time == timedelta(seconds=(1 * 60 * 60 + 20 * 60 + 4.03))
    assert mark.name == "video start"


def test_init_valid_start():
    mark = Mark(1, timedelta(seconds=0.03), "video start")
    assert mark.frame == 1
    assert mark.time == timedelta(seconds=0.03)
    assert mark.name == "video start"


def test_init_valid_end():
    mark = Mark(54001, timedelta(seconds=(30 * 60 + 0.03)), "video end")
    assert mark.frame == 54001
    assert mark.time == timedelta(seconds=(30 * 60 + 0.03))
    assert mark.name == "video end"


def test_init_valid_long_time():
    mark = Mark(1, timedelta(seconds=(1 * 60 * 60 + 20 * 60 + 4.03)),
                "video start")
    assert mark.frame == 1
    assert mark.time == timedelta(seconds=(1 * 60 * 60 + 20 * 60 + 4.03))
    assert mark.name == "video start"


def test_to_line_valid_start_end_is_template():
    start = "    1     0:00.03    video start"
    end = "54001    30:00.03    video end"
    mark = Mark.from_line(start)
    assert mark.to_line(end) == start


def test_to_line_valid_end_start_is_template():
    start = "    1     0:00.03    video start"
    end = "54001    30:00.03    video end"
    mark = Mark.from_line(end)
    assert mark.to_line(start) == end


def test_to_line_valid_hours():
    temp = " 54001    30:00.03    video end"
    mark = Mark(17, timedelta(seconds=3650.05), "weird mark")
    assert mark.to_line(temp) == "    17  1:00:50.05    weird mark"


def test_to_line_valid_secs():
    temp = " 54001    30:00.03    video end"
    mark = Mark(17, timedelta(seconds=4.05), "weird mark")
    assert mark.to_line(temp) == "    17     0:04.05    weird mark"


def test_to_line_valid_microsecs():
    temp = " 54001    30:00.03    video end"
    mark = Mark(17, timedelta(seconds=0.05), "weird mark")
    assert mark.to_line(temp) == "    17     0:00.05    weird mark"


def test_to_line_valid_long_frame():
    temp = " 54001    30:00.03    video end"
    mark = Mark(143063, timedelta(seconds=4.05), "weird mark")
    assert mark.to_line(temp) == "143063     0:04.05    weird mark"


def test_to_line_valid_one_word_name():
    temp = " 54001    30:00.03    video end"
    mark = Mark(17, timedelta(seconds=4.05), "mark")
    assert mark.to_line(temp) == "    17     0:04.05    mark"


def test_to_line_valid_one_word_name_in_template():
    temp = " 54001    30:00.03    videoend"
    mark = Mark(17, timedelta(seconds=4.05), "weird mark")
    assert mark.to_line(temp) == "    17     0:04.05    weird mark"


def test_to_line_valid_long_frame_in_template():
    temp = "154001    30:00.03    video end"
    mark = Mark(17, timedelta(seconds=4.05), "weird mark")
    assert mark.to_line(temp) == "    17     0:04.05    weird mark"


def test_to_line_invalid_template_1_space_after_frame():
    with pytest.raises(ValueError):
        mark = Mark(1, timedelta(seconds=1), "mark")
        mark.to_line("    1 0:00.03    video start")


def test_to_line_invalid_template_1_space_after_time():
    with pytest.raises(ValueError):
        mark = Mark(1, timedelta(seconds=1), "mark")
        mark.to_line("    1     0:00.03 video start")


def test_to_line_invalid_time_over_1_day():
    with pytest.raises(ValueError):
        mark = Mark(17, timedelta(days=1.05), "weird mark")
        mark.to_line(" 54001    30:00.03    video end")


def test_to_line_valid_remove_leading_zero_minutes():
    temp = " 54001    30:00.03    video end"
    mark = Mark(17, timedelta(seconds=61.05), "weird mark")
    assert mark.to_line(temp) == "    17     1:01.05    weird mark"


def test_to_line_valid_remove_leading_zero_hours():
    temp = " 54001    30:00.03    video end"
    mark = Mark(17, timedelta(seconds=3601.05), "weird mark")
    assert mark.to_line(temp) == "    17  1:00:01.05    weird mark"


def test_lt_frame_positive():
    first = Mark.from_line("    1     0:00.03    video start")
    second = Mark.from_line("    2     0:00.03    video start")

    assert first < second


def test_lt_frame_negative():
    first = Mark.from_line("    -2     0:00.03    video start")
    second = Mark.from_line("    -1     0:00.03    video start")

    assert first < second


def test_lt_frame_both_signs():
    first = Mark.from_line("    -1     0:00.03    video start")
    second = Mark.from_line("    1     0:00.03    video start")

    assert first < second


def test_lt_time_positive():
    first = Mark.from_line("    1     0:00.03    video start")
    second = Mark.from_line("    1     0:05.00    video start")

    assert first < second


def test_lt_time_negative():
    first = Mark.from_line("    1     -0:05.00    video start")
    second = Mark.from_line("    1     -0:00.03    video start")

    assert first < second


def test_lt_time_both_signs():
    first = Mark.from_line("    1     -0:00.03    video start")
    second = Mark.from_line("    1     0:00.03    video start")

    assert first < second


def test_lt_name():
    first = Mark.from_line("    1     0:00.03    a video starts")
    second = Mark.from_line("    1     0:00.03    video start")

    assert first < second


def test_lt_name_lexicographic():
    first = Mark.from_line("    1     0:00.03    A video starts")
    second = Mark.from_line("    1     0:00.03    video starts")

    assert first < second


def test_lt_equal():
    first = Mark.from_line("    1     0:00.03    A video starts")
    second = Mark.from_line("    1     0:00.03    A video starts")

    assert first >= second
