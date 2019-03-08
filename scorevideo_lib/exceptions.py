# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""Custom exceptions

"""

class FileFormatError(Exception):
    """Raised when a file is improperly formatted.

    The message should describe the file and how it is mis-formatted.
    """

    @staticmethod
    def from_lines(filename, found_line, expected_line):
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
        return FileFormatError(message)
