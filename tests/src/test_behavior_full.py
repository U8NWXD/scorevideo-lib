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

"""Unit tests for the :py:class:BehaviorFull class

"""

import pytest
from scorevideo_lib.parse_log import BehaviorFull

TEST_RES = "tests/res"

# pragma pylint: disable=missing-docstring


def test_init_invalid_time_two_decimal_points():
    with pytest.raises(TypeError):
        BehaviorFull("  171     0.05.70    Pot entry exit          either")


def test_init_invalid_raw_behavior():
    with pytest.raises(TypeError):
        BehaviorFull("53946     29:58.20     C")


def test_init_invalid_time_no_decimal_points():
    with pytest.raises(TypeError):
        BehaviorFull("  171     0:05:70    Pot entry exit          either")


def test_init_invalid_no_description():
    with pytest.raises(TypeError):
        BehaviorFull("  171     0:05.70              either")


def test_init_valid_negative_frame():
    BehaviorFull("  -171     0:05.70    Pot entry exit          either")


def test_init_valid_negative_time():
    BehaviorFull("  171     -0:05.70    Pot entry exit          either")


def test_init_invalid_nonnumeric_frame():
    with pytest.raises(TypeError):
        BehaviorFull("  17a1     0:05.70    Pot entry exit          either")


def test_init_invalid_nonnumeric_time():
    with pytest.raises(TypeError):
        BehaviorFull("  171     a0:05.70    Pot entry exit          either")


def test_init_invalid_no_frame():
    with pytest.raises(TypeError):
        BehaviorFull("       0:05.70    Pot entry exit          either")


def test_init_invalid_no_time():
    with pytest.raises(TypeError):
        BehaviorFull("  171         Pot entry exit          either")


def test_init_invalid_no_either():
    with pytest.raises(TypeError):
        BehaviorFull("  171     0:05.70    Pot entry exit          ")


def test_init_invalid_one_space():
    with pytest.raises(TypeError):
        BehaviorFull("  171     0:05.70 Pot entry exit          either")


def test_init_invalid_5_elems():
    with pytest.raises(TypeError):
        BehaviorFull("|  171   0:05.70  Pot entry exit   either  ")


def test_init_invalid_behavior():
    with pytest.raises(TypeError):
        BehaviorFull("  171     0:05.70  Pot entry exit!          either")


def test_init_invalid_subject():
    with pytest.raises(TypeError):
        BehaviorFull("  171     0:05.70  Pot entry exit          both")


def test_init_valid_normal():
    BehaviorFull("  171     28:52.70    Pot entry exit          either")


def test_init_valid_short_time():
    BehaviorFull("  171     0:05.70    Pot entry exit          either")


def test_init_valid_long_time():
    BehaviorFull("  171     0:01:05.70    Pot entry exit          either")


def test_lt_frame_positive():
    one = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")
    two = BehaviorFull("  173     0:01:05.70    Pot entry exit      either")

    assert one < two


def test_lt_frame_negative():
    one = BehaviorFull("  -173     0:01:05.70    Pot entry exit      either")
    two = BehaviorFull("  -171     0:01:05.70    Pot entry exit      either")

    assert one < two


def test_lt_frame_both_signs():
    one = BehaviorFull("  -171     0:01:05.70    Pot entry exit      either")
    two = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")

    assert one < two


def test_lt_time_positive():
    one = BehaviorFull("  171     0:00:05.70    Pot entry exit      either")
    two = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")

    assert one < two


def test_lt_time_negative():
    one = BehaviorFull("  171     -0:01:05.70    Pot entry exit      either")
    two = BehaviorFull("  171     -0:00:05.70    Pot entry exit      either")

    assert one < two


def test_lt_time_both_signs():
    one = BehaviorFull("  171     -0:01:05.70    Pot entry exit      either")
    two = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")

    assert one < two


def test_lt_description():
    one = BehaviorFull("  171     0:01:05.70    Aot entry exit      either")
    two = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")

    assert one < two


def test_lt_description_lexicographic():
    one = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")
    two = BehaviorFull("  171     0:01:05.70    pot entry exit      either")

    assert one < two


def test_lt_subject():
    one = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")
    one.subject = "aeither"  # Needed to avoid validator rejecting subject
    two = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")

    assert one < two


def test_lt_subject_lexicographic():
    one = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")
    one.subject = "Either"  # Needed to avoid validator rejecting subject
    two = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")

    assert one < two


def test_lt_equal():
    one = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")
    two = BehaviorFull("  171     0:01:05.70    Pot entry exit      either")

    assert one >= two
