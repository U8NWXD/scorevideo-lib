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

"""Test log file parsing

"""

from scorevideo_lib.parse_log import Log

TEST_RES = "tests/res"

def get_actual_expected(expected_path, extractor, source_path):
    """Get the actual and expected outputs from section extraction methods

    Args:
        expected_path: Path to the file containing the expected section
        extractor: Method to use to extract the section from source_path
        source_path: Path to the log file to attempt extraction from

    Returns: (expected, actual) where expected is a list of the expected lines
    and actual is the list of lines actually extracted by extractor

    """
    with open(expected_path, 'r') as file:
        expected = [line.rstrip() for line in file.readlines()]
    with open(source_path, 'r') as source:
        actual = extractor(source)
    return expected, actual

def test_get_section_header_all():
    """Test that the header can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/header.txt",
                                   Log.get_section_header,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_video_info_all():
    """Test that the video info section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/video_info.txt",
                                   Log.get_section_video_info,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_commands_all():
    """Test that the commands section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/comm.txt",
                                   Log.get_section_commands,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_raw_all():
    """Test that the raw log section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/raw.txt",
                                   Log.get_section_raw,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_full_all():
    """Test that the full log section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/full.txt",
                                   Log.get_section_full,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_notes_all():
    """Test that the notes section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/notes.txt",
                                   Log.get_section_notes,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_marks_all():
    """Test that the marks section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/marks.txt",
                                   Log.get_section_marks,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act
