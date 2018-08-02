TEST_RES = "tests/res"

def test_file_read():
    expected = ["scorevideo LOG\n", "File:  log.mat"]
    with open(TEST_RES + "/file_read.txt", 'r') as file:
        actual = file.readlines()
    assert expected == actual
