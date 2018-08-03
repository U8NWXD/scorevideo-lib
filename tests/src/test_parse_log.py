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

def test_get_section_header_all():
    """Test that the header can be extracted from a normal log file

    Returns: None

    """
    with open(TEST_RES + "/expectedLogParts/header.txt", 'r') as file:
        expected = [line.rstrip() for line in file.readlines()]
    with open(TEST_RES + "/realisticLogs/all.txt", 'r') as file:
        actual = Log.get_section_header(file)

    assert expected == actual

def test_get_section_video_info_all():
    """Test that the video info section can be extracted from a normal log file

    Returns: None

    """
    with open(TEST_RES + "/expectedLogParts/video_info.txt", 'r') as file:
        expected = [line.rstrip() for line in file.readlines()]
    with open(TEST_RES + "/realisticLogs/all.txt", 'r') as file:
        actual = Log.get_section_video_info(file)

    assert expected == actual
