# `scorevideo_lib`: Scorevideo Library
[![Build Status](https://travis-ci.com/U8NWXD/scorevideo_lib.svg?branch=master)](https://travis-ci.com/U8NWXD/scorevideo_lib)
[![codecov](https://codecov.io/gh/U8NWXD/scorevideo_lib/branch/master/graph/badge.svg)](https://codecov.io/gh/U8NWXD/scorevideo_lib)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.png?v=103)](LICENSE.txt)

Library of utilities for working with the MATLAB program
`scorevideo`.

## Development Status
`scorevideo_lib` is in development and should not be relied upon for
critical tasks. It is, however, useful for a limited set of tasks.

## Code Style
Python code should conform to the 
[PEP8](https://www.python.org/dev/peps/pep-0008/) style guidelines.

Docstrings should conform to the 
[Google Style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).
For example (copied from 
[Google's Style Guide](https://github.com/google/styleguide)):
```python
def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
```

## Testing
To run all tests, execute `test.sh`. These tests are checked are run by 
[Travis CI](https://travis-ci.com) on all pull requests and the master branch. 
Before each commit, run `test.sh` and ensure that all tests pass. All tests
should pass on each commit to make reverting easy.

### Unit Testing
Unit testing is performed using [`pytest`](https://pytest.org/). To run these 
tests, execute `python -m pytest` from the repository root.

### Code and Style Analysis
PEP8 are checked by `pylint`.
`pylint` also performs static code analysis to catch some programming errors. 
This analysis is intended to be a fall-back defense, as unit testing should be 
thorough.

### Type Checking
All code should use type hints wherever type cannot be inferred. At a minimum,
all function prototypes should have type hints for the return value and each
parameter. Type hinting is performed in the code itself, not in docstrings.
Static type analysis is performed by `mypy`

### Code Coverage
When running the test suite using `test.sh`, code coverage is computed by 
[`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/) when running 
`pytest` and output after test results. Use these results to ensure that all 
tests are being covered. If the total coverage is not `100%`, run 
`coverage report -m` to see which lines were not tested. Incomplete coverage 
may be acceptable if the untested lines should not have been tested (e.g. code 
stubs for un-implemented functions).

Coverage is tracked by [Codecov](https://codecov.io), which serves the badge at
the top of this README.

## License and Copyright
Use of this repository is governed by the license in [LICENSE.txt](LICENSE.txt)