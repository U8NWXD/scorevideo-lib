TEST_RES = "tests/res"

from scorevideo_lib.parse_log import Log

def test_file_read():
    expected = ["scorevideo LOG", "File:  log.mat"]
    with open(TEST_RES + "/file_read.txt", 'r') as f:
        actual = f.readlines()
    assert(expected == actual)

def test_get_section_header_all():
    with open(TEST_RES + "/expectedLogParts/header.txt", 'r') as f:
        expected = f.readlines()

    with open(TEST_RES + "/realisticLogs/all.txt", 'r') as f:
        actual = Log.get_section_header(f)

    assert(expected == actual)