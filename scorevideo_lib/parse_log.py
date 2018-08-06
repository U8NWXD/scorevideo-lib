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

"""Parse log files

"""

from scorevideo_lib.exceptions import FileFormatError


class Log:
    """Store an interpreted form of a log file and perform operations on it

    Attributes:
        log_file: Reference to the open log file. May need to be re-wound
        header: List of the lines in the header section
        video_info: List of the lines in the video info section
        commands: List of the lines in the commands section
        raw: List of the lines in the raw log section
        full: List of the lines in the full log section
        notes: List of the lines in the notes section
        marks: List of the lines in the marks section
    """

    # pylint: disable=too-many-instance-attributes
    # In this case, it is reasonable to have an instance attribute per section

    def __init__(self, log_file):
        """Parse log file into its sections.

        Populate the attributes of the Log class by using the get_section_*
        static methods to extract sections that are stored in attributes.

        Args:
            log_file: An open file object that points to the log file to read.
        """
        self.log_file = log_file
        self.header = Log.get_section_header(log_file)
        self.video_info = Log.get_section_video_info(log_file)
        self.commands = Log.get_section_commands(log_file)
        self.raw = Log.get_section_raw(log_file)
        self.full = Log.get_section_full(log_file)
        self.notes = Log.get_section_notes(log_file)
        self.marks = Log.get_section_marks(log_file)
        log_file.seek(0)

    @staticmethod
    def get_section_header(log_file):
        """Get the header section of a log.

        Extract the top section (top two lines) of a log. This section includes
        a statement that the log was created by
        scorevideo and the name of the log file.

        Args:
            log_file: An open file object that points to the log file to read.
            The file object must be ready to be read,
                and it should be at the start of the file.

        Returns:
            A list of the lines making up the header in sequential order, with
            each line a separate element in the list.
            Newlines or return carriages are stripped from the ends of lines.
        """
        header = []
        for _ in range(2):
            header.append(log_file.readline().rstrip())
        return header

    @staticmethod
    def get_section_video_info(log_file):
        """Get the video info section of a log.

        Extract the video info section (headed by the line "VIDEO FILE SET" of a
        log. This section includes
        information about the video including format, directory, name, start and
        end frames, duration, frame
        rate (FPS), and number of subjects

        Args:
            log_file: An open file object that points to the log file to read.
                The file object must be ready to be read,
                and it should be at the start of the file.
        Returns:
            A list of the lines making up the section in sequential order, with
            each line a separate element in the list.
            Newlines or return carriages are stripped from the ends of lines.
        """
        return Log.get_section(log_file, "VIDEO FILE SET", [], "")

    @staticmethod
    def get_section_commands(log_file):
        """Get the commands section of a log.

        Extract the commands section (headed by the line "COMMAND SET AND
        SETTINGS") used in generating the log file.
        This section specifies the key commands (letters) used to signal the
        beginning and end of each behavior.

        Args:
            log_file: An open file object that points to the log file to read.
                The file object must be ready to be read,
                and it should be at the start of the file.
        Returns:
            A list of the lines making up the section in sequential order, with
            each line a separate element in the list.
            Newlines or return carriages are stripped from the ends of lines.
        """
        header = ["-------------------------------",
                  "start|stop|subject|description",
                  "-------------------------------"]
        end = "-------------------------------"
        return Log.get_section(log_file, "COMMAND SET AND SETTINGS", header,
                               end)

    @staticmethod
    def get_section_raw(log_file):
        """Get the raw log section of a log.

        Extract the section of the log that contains the raw scoring log. This
        section contains the frame number and
        time of each scored behavior along with the key command that was scored
        for that behavior

        Args:
            log_file: An open file object that points to the log file to read.
                The file object must be ready to be read,
                and it should be at the start of the file.
        Returns:
            A list of the lines making up the section in sequential order, with
            each line a separate element in the list.
            Newlines or return carriages are stripped from the ends of lines.
        """
        header = ["------------------------------------------",
                  "frame|time(min:sec)|command",
                  "------------------------------------------"]
        end = "------------------------------------------"
        return Log.get_section(log_file, "RAW LOG", header, end)

    @staticmethod
    def get_section_full(log_file):
        """Get the full log section of a log.

        Extract the section of the log that contains the full scoring log. This
        section contains the frame number and
        time of each scored behavior along with the full name assigned to that
        behavior in the commands section

        Args:
            log_file: An open file object that points to the log file to read.
                The file object must be ready to be read,
                and it should be at the start of the file.
        Returns:
            A list of the lines making up the section in sequential order, with
            each line a separate element in the list.
            Newlines or return carriages are stripped from the ends of lines.
        """
        header = ["------------------------------------------",
                  "frame|time(min:sec)|description|action|subject",
                  "------------------------------------------"]
        end = "------------------------------------------"
        return Log.get_section(log_file, "FULL LOG", header, end)

    @staticmethod
    def get_section_notes(log_file):
        """Get the notes section of a log.

        Extract the notes section of the log, which contains arbitrary notes
        specified by the researcher during scoring,
        one per line.

        Args:
            log_file: An open file object that points to the log file to read.
                The file object must be ready to be read,
                and it should be at the start of the file.
        Returns:
            A list of the lines making up the section in sequential order, with
            each line a separate element in the list.
            Newlines or return carriages are stripped from the ends of lines.
        """
        end = "------------------------------------------"
        header = ["------------------------------------------"]
        return Log.get_section(log_file, "NOTES", header, end)

    @staticmethod
    def get_section_marks(log_file):
        """Get the marks section of a log.

        Extract the marks section of the log, which stores the frame number and
        time at which the video starts and stops.
        Additional marks can be added here, such as when statistical analysis
        should begin or when fish started behaving.

        Args:
            log_file: An open file object that points to the log file to read.
                The file object must be ready to be read,
                and it should be at the start of the file.
        Returns:
            A list of the lines making up the section in sequential order, with
            each line a separate element in the list.
            Newlines or return carriages are stripped from the ends of lines.
        """
        header = ["------------------------------------------",
                  "frame|time(min:sec)|mark name",
                  "------------------------------------------"]
        end = "------------------------------------------"
        return Log.get_section(log_file, "MARKS", header, end)

    @staticmethod
    def get_section(log_file, start, header, end):
        """Get an arbitrary section from a log file.

        Extract an arbitrary section from a log file. The section is defined by
        a line at its start and a line at its end, neither of which are
        considered part of the section (not returned). A header section is also
        specified, the lines of which will be checked and excluded from the
        section. A header starts on the line immediately following the start
        line. If the header is not found, or if a line in it does not match, a
        FileFormatError is raised. If the end of the file is unexpectedly found
        before completing a section, a FileFormatError is raised.

        Args:
            log_file: An open file object that points to the log file to read.
                The file object must be ready to be read,
                and it should be at the start of the file.
            start: Line that signals the start of the section
            header: List of lines that form a header to the section. If no
                header should be present, pass an empty list.
            end: Line that signals the end of the section

        Returns:
            A list of the lines making up the section in sequential order, with
            each line a separate element in the list.
            Newlines or return carriages are stripped from the ends of lines.
        """
        line = log_file.readline()
        while line.rstrip() != start:
            if line == "":
                raise FileFormatError("The start line '" + start +
                                      "' was not found in " + log_file.name)
            else:
                line = log_file.readline()
        for header_line in header:
            found_line = log_file.readline().rstrip()
            if header_line != found_line:
                raise FileFormatError.from_lines(log_file.name, found_line,
                                                 header_line)
        section = []
        line = log_file.readline()
        while not line.rstrip() == end:
            if line == "":
                raise FileFormatError("The end line '" + end +
                                      "' was not found in " + log_file.name)
            line = line.rstrip()
            section.append(line)
            line = log_file.readline().rstrip()

        return section
