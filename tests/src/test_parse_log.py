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
from scorevideo_lib.exceptions import FileFormatError

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

def test_get_section_raw_no_behavior():
    """Get the raw log section of a log that has no behavior recorded

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/blank.txt",
                                   Log.get_section_raw,
                                   TEST_RES + "/realisticLogs/noBehavior.txt")
    assert exp == act

def test_get_section_full_all():
    """Test that the full log section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/full.txt",
                                   Log.get_section_full,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_full_no_behavior():
    """Get the full log section of a log that has no behavior recorded

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/blank.txt",
                                   Log.get_section_full,
                                   TEST_RES + "/realisticLogs/noBehavior.txt")
    assert exp == act

def test_get_section_notes_all():
    """Test that the notes section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/notes.txt",
                                   Log.get_section_notes,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_notes_no_notes():
    """Get the notes section of a log that has no notes recorded

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/blank.txt",
                                   Log.get_section_notes,
                                   TEST_RES + "/realisticLogs/noNotes.txt")
    assert exp == act

def test_get_section_marks_all():
    """Test that the marks section can be extracted from a normal log file

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/expectedLogParts/marks.txt",
                                   Log.get_section_marks,
                                   TEST_RES + "/realisticLogs/all.txt")

    assert exp == act

def test_get_section_missing_end():
    """Test handling of section ends that aren't found.

    Test that a FileFormatError with the proper message is raised when the line
    thought to signal the end of the section is never found.

    Returns: None

    """
    failed = False
    with open(TEST_RES + "/realisticLogs/all.txt", 'r') as file:
        try:
            Log.get_section(file, "RAW LOG", [], "-----")
        except FileFormatError as error:
            assert str(error) == "The end line '-----' was not found in " \
                                 "tests/res/realisticLogs/all.txt"
            failed = True
    assert failed

def test_get_section_missing_start():
    """Test handling of section starts that aren't found.

    Test that a FileFormatError with the proper message is raised when the line
    thought to signal the start of the section is never found.

    Returns: None

    """
    failed = False
    with open(TEST_RES + "/realisticLogs/all.txt", 'r') as file:
        try:
            Log.get_section(file, "-----", [], "RAW LOG")
        except FileFormatError as error:
            assert str(error) == "The start line '-----' was not found in " \
                                 "tests/res/realisticLogs/all.txt"
            failed = True
    assert failed

def test_get_section_missing_header():
    """Test handling of section headers that don't match what is expected.

    Test that a FileFormatError with the proper message is raised when there is
    a difference in the expected header and the header actually found.

    Returns: None

    """
    failed = False
    headers = ["------------------------------------------",
               "frame|time(min:sec)|command",
               "---"]
    end = "------------------------------------------"
    exp = FileFormatError.from_lines("tests/res/realisticLogs/all.txt",
                                     "------------------------------------------",
                                     "---")
    with open(TEST_RES + "/realisticLogs/all.txt", 'r') as file:
        try:
            Log.get_section(file, "RAW LOG", headers, end)
        except FileFormatError as error:
            assert str(error) == str(exp)
            failed = True
    assert failed
