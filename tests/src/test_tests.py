TEST_RES = "tests/res"

def test_file_read():
    expected = ["scorevideo LOG\r\n", "File:  log.mat"]
    with open(TEST_RES + "/file_read.txt", 'r') as f:
        actual = f.readlines()
    assert(expected == actual)