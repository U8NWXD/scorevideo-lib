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

"""Test operations needed to run other tests.

"""

from tests.src.test_rawlog import get_actual_expected

TEST_RES = "tests/res"


def test_file_read():
    """Test that file reading works.

    Tests that lines with and without trailing newlines are extracted verbatim
    from files as performed by other tests.

    Returns: None

    """
    expected = ["scorevideo LOG\n", "File:  log.mat"]
    with open(TEST_RES + "/file_read.txt", 'r') as file:
        actual = file.readlines()
    assert expected == actual


def return_file_read(_):
    """Return the lines expected to be found in the file_read test file.

    Args:
        _: Present to mimic the behavior of RawLog.get_section_* functions, but not
            used by the function

    Returns: A list of the lines in file_read.txt with trailing whitespace
    removed

    """
    return ["scorevideo LOG", "File:  log.mat"]


def test_get_actual_expected():
    """Test that the get_actual_expected function works.

    This is important because other functions use get_actual_expected

    Returns: None

    """
    exp, act = get_actual_expected(TEST_RES + "/file_read.txt",
                                   return_file_read,
                                   TEST_RES + "/file_read.txt")
    assert exp == act
