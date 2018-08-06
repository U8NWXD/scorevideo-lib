# `scorevideo_lib`: Scorevideo Library
[![Build Status](https://travis-ci.com/U8NWXD/scorevideo_lib.svg?branch=master)](https://travis-ci.com/U8NWXD/scorevideo_lib)
[![codecov](https://codecov.io/gh/U8NWXD/scorevideo_lib/branch/master/graph/badge.svg)](https://codecov.io/gh/U8NWXD/scorevideo_lib)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.png?v=103)](LICENSE.txt)

Library of utilities for working with the MATLAB program
`scorevideo`.

## Development Status
`scorevideo_lib` is still in early development and has not yet had an alpha 
release.

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
Copyright (c) 2018  U8N WXD <cs.temporary@icloud.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.