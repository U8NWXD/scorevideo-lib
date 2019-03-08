# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""Test the :py:class:Log class

"""

from datetime import timedelta
from scorevideo_lib.parse_log import Log, BehaviorFull, Mark, RawLog
from tests.src import TEST_RES

# pragma pylint: disable=missing-docstring


def test_constructor():
    log = Log()
    assert log.full == [BehaviorFull(" 0  00:00.00  null  either ")]
    assert log.marks == [Mark(0, timedelta(0), "")]


def test_from_log():
    log = Log()
    copy = Log.from_log(log)

    assert log.full == copy.full
    assert log.full is not copy.full

    assert log.marks == copy.marks
    assert log.marks is not copy.marks


def test_from_rawlog():
    str_full = " 0  00:00.00  null  either "
    str_mark = "    1     0:00.03    video start"

    rawlog = RawLog()
    rawlog.full.append(str_full)
    rawlog.marks.append(str_mark)

    log = Log.from_raw_log(rawlog)

    assert log.full == [BehaviorFull(" 0  00:00.00  null  either ")]
    assert log.marks == [Mark.from_line("    1     0:00.03    video start")]


def test_from_file():
    with open(TEST_RES + "/realisticLogs/all.txt") as f:
        auto = Log.from_file(f)
        manual = Log.from_raw_log(RawLog.from_file(f))
    assert auto.full == manual.full
    assert auto.marks == manual.marks
