TEST_RES = "tests/res"

from scorevideo_lib.parse_log import Log

def test_get_section_header_all():
    with open(TEST_RES + "/expectedLogParts/header.txt", 'r') as f:
        expected = f.readlines()

    with open(TEST_RES + "/realisticLogs/all.txt", 'r') as f:
        actual = Log.get_section_header(f)

    assert(expected == actual)