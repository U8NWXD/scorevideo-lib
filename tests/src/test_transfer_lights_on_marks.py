# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""Tests for the :py:mod:`transfer_lights_on_marks` tool

"""

import os
from shutil import copytree, rmtree
from pytest import fixture
from scorevideo_lib.transfer_lights_on_marks import batch_mark_lights_on
from tests.src import TEST_RES

# pragma pylint: disable=missing-docstring
# pragma pylint: disable=redefined-outer-name
# Pytest requires that when fixtures are used as parameters, they have the same
# name as the fixture


@fixture
def temp_test_dir():
    src = os.path.join(TEST_RES, "lightsOn")
    dst = os.path.join(TEST_RES, "tmp")
    copytree(src, dst)
    yield src, dst
    rmtree(dst)


def lights_on_test_helper(temp_test_dir, scored_name, expected_mark):
    src, dst = temp_test_dir
    batch_mark_lights_on(dst)
    with open(os.path.join(dst, scored_name)) as actual_file:
        with open(os.path.join(src, scored_name)) as expected_file:
            actual = actual_file.readlines()
            expected = expected_file.readlines()
            expected.insert(len(expected) - 1, expected_mark)
    assert actual == expected


def test_mark_lights_on(temp_test_dir):
    scored_name = "log050118_OD1030618_TA23_Dyad_Morning.avi_CS.txt"
    expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
    lights_on_test_helper(temp_test_dir, scored_name, expected_mark)


def test_mark_lights_on_no_behav_1st(temp_test_dir):
    scored_name = "log120118_OD1030618_OC4A_Dyad_Morning.avi_CS.txt"
    expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
    lights_on_test_helper(temp_test_dir, scored_name, expected_mark)


def test_mark_lights_on_no_behav_scored(temp_test_dir):
    scored_name = "log120118_OD1100618_OC4A_Dyad_Morning.avi_CS.txt"
    expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
    lights_on_test_helper(temp_test_dir, scored_name, expected_mark)


def test_mark_lights_on_empty_1st_neg_behav(temp_test_dir):
    scored_name = "log050118_OB5B030618_TA23_Dyad_Morning.avi_CS.txt"
    expected_mark = "-72820   -40:27.33    LIGHTS ON\n"
    lights_on_test_helper(temp_test_dir, scored_name, expected_mark)
