# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""Test operations needed to run other tests.

"""

from tests.src.test_rawlog import get_actual_expected
from tests.src import TEST_RES


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
