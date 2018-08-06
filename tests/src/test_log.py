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

"""Test the Log class

"""

from scorevideo_lib.parse_log import Log

TEST_RES = "tests/res"


def test_constructor_all():
    """Test creating a Log object from a full log

    Creates a Log object from a full test log (all.txt) and then compares the
    resulting object's attributes to the contents of the files in
    expectedLogParts.

    Returns: None

    """
    with open(TEST_RES + "/realisticLogs/all.txt", 'r') as log_all:
        log = Log(log_all)

    tests = [("header.txt", log.header), ("video_info.txt", log.video_info),
             ("comm.txt", log.commands), ("raw.txt", log.raw),
             ("full.txt", log.full), ("notes.txt", log.notes),
             ("marks.txt", log.marks)]

    for file, found in tests:
        with open(TEST_RES + "/expectedLogParts/" + file, 'r') as part_file:
            expected = [line.rstrip() for line in part_file]
        assert found == expected


def test_constructor_no_notes():
    """Test creating a Log object from a log with no notes

        Creates a Log object from a test log without notes(noNotes.txt) and then
        compares the resulting object's attributes to the contents of the files
        in expectedLogParts.

        Returns: None

        """
    with open(TEST_RES + "/realisticLogs/noNotes.txt", 'r') as log_all:
        log = Log(log_all)

    tests = [("header.txt", log.header), ("video_info.txt", log.video_info),
             ("comm.txt", log.commands), ("raw.txt", log.raw),
             ("full.txt", log.full), ("blank.txt", log.notes),
             ("marks.txt", log.marks)]

    for file, found in tests:
        with open(TEST_RES + "/expectedLogParts/" + file, 'r') as part_file:
            expected = [line.rstrip() for line in part_file]
        assert found == expected
