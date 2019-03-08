# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""Unit tests for the ``add_marks`` file

"""

from datetime import timedelta
import pytest
from scorevideo_lib.add_marks import copy_mark_disjoint, get_ending_mark
from scorevideo_lib.parse_log import Log, RawLog, Mark
from tests.src import TEST_RES

# pragma pylint: disable=missing-docstring


def test_add_lights_on_mark_correct():
    dest_label = "Lights On"
    with open(TEST_RES + "/realisticLogs/lights_on.txt", "r") as file:
        source = Log.from_file(file)
    with open(TEST_RES + "/realisticLogs/all.txt", "r") as file:
        middle = Log.from_file(file)
    with open(TEST_RES + "/realisticLogs/all.txt", "r") as file:
        destination = RawLog.from_file(file)

    frame_diff = 54001 + 54001 - 12331 + 54001
    # pylint: disable=bad-continuation
    time_diff = timedelta(minutes=30, seconds=0.03) + \
                timedelta(minutes=30, seconds=0.03) - \
                timedelta(minutes=6, seconds=51.03) + \
                timedelta(minutes=30, seconds=0.03)
    with open(TEST_RES + "/realisticLogs/all.txt", "r") as file:
        expected = RawLog.from_file(file)
    new_mark = Mark(-frame_diff, -time_diff, dest_label)
    expected.marks.append(new_mark.to_line(expected.marks[0]))

    actual = copy_mark_disjoint([source, middle, middle], "Lights On",
                                destination, dest_label)

    assert expected.marks == actual.marks
    assert "-" in expected.marks[-1]


def test_add_lights_on_nondisjoint_correct():
    pass # TODO: Write this test for add_lights non-disjoint


def test_missing_start_mark():
    with pytest.raises(ValueError):
        get_ending_mark([Mark(0, timedelta(seconds=0), "foo")])
