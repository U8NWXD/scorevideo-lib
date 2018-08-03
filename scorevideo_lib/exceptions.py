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

"""Custom exceptions

"""

class FileFormatError(Exception):
    """Raised when a file is improperly formatted.

    The message should describe the file and how it is mis-formatted.
    """

    @classmethod
    def from_lines(cls, filename, found_line, expected_line):
        """Create new object with message from parameters.

        Args:
            filename: Name of file that is improperly formatted
            found_line: The line that was found in the file
            expected_line: The line that was expected to be found

        Returns: None

        """
        message = "In the file '" + filename + "', the line '" + \
                  found_line + "' was found instead of the expected '" + \
                  expected_line + "'."
        super().__init__(message)
