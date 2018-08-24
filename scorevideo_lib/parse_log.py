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

from typing import List
import re
from datetime import timedelta
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

    def __init__(self, log_file) -> None:
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
    def get_section_header(log_file) -> List[str]:
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
    def get_section_video_info(log_file) -> List[str]:
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
    def get_section_commands(log_file) -> List[str]:
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
    def get_section_raw(log_file) -> List[str]:
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
    def get_section_full(log_file) -> List[str]:
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
    def get_section_notes(log_file) -> List[str]:
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
    def get_section_marks(log_file) -> List[str]:
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
    def get_section(log_file, start: str, header: List[str], end: str) \
            -> List[str]:
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


class BehaviorFull:
    """Store an interpreted representation of a behavior from the full section

    Attributes:
        frame: A positive integer representing the frame number on which the
            behavior was scored.
        time: A :py:class:timedelta object that represents the time elapsed
            from the start of the clip to the behavior being scored. This is a
            representation of the time listed in the log line.
        description: The name of the behavior that appears as the second-to-last
            element in the provided line
        subject: Always the string ``either``
    """

    def __init__(self, behavior_line: str) -> None:
        """Create a new :py:class:`BehaviorFull` object from the provided line.

        >>> behav = BehaviorFull(" 1769  0:58.97  Flee from male  either ")
        >>> behav.frame
        1769
        >>> behav.time
        datetime.timedelta(seconds=58, microseconds=970000)
        >>> behav.description
        'Flee from male'
        >>> behav.subject
        'either'

        Args:
            behavior_line: A line from the ``FULL LOG`` section of a log file
        Returns:
            None
        Raises:
            TypeError: When the provided line does not conform to the
                expected format. Notably, all 4 elements of the line must be
                separated from each other by at least 2 spaces.
        """
        split = re.split(r"\s{2,}", behavior_line)
        split[0] = split[0].lstrip()
        split[-1] = split[-1].rstrip()
        line = [elem for elem in split if elem != ""]
        line_error = "The line '" + behavior_line + "' is not a valid line " \
                                                    "from the FULL LOG section"
        if len(line) > 4:
            err = "{} (num elements: {} > 4)".format(line_error, len(line))
            raise TypeError(err)
        elif len(line) < 4:
            err = "{} (num elements: {} < 4)".format(line_error, len(line))
            raise TypeError(err)
        elif not BehaviorFull.validate_frame(line[0]):
            err = "{} ('{}' is not a valid frame number)".format(line_error,
                                                                 line[0])
            raise TypeError(err)
        elif not BehaviorFull.validate_time(line[1]):
            err = "{} ('{}' is not a valid time)".format(line_error, line[1])
            raise TypeError(err)
        elif not BehaviorFull.validate_behavior(line[2]):
            err = "{} ('{}' is not a valid behavior)".format(line_error,
                                                             line[2])
            raise TypeError(err)
        elif not BehaviorFull.validate_subject(line[3]):
            err = "{} ('{}' is not a valid subject)".format(line_error, line[3])
            raise TypeError(err)

        self.frame = int(line[0])
        split_time = line[1].split(":")
        secs = float(split_time[-1])
        # MM:SS.SS -> [MM, SS.SS]
        if len(split_time) == 2:
            secs += int(split_time[0]) * 60
        # HH:MM:SS.SS -> [HH, MM, SS.SS]
        elif len(split_time) == 3:
            secs += int(split_time[0]) * 60 * 60
            secs += int(split_time[1]) * 60
        self.time = timedelta(seconds=secs)
        self.description = line[2]
        self.subject = line[3]

    @staticmethod
    def validate_frame(frame: str) -> bool:
        """Check whether ``frame`` represents a valid frame number

        A valid frame number is any non-negative integer. Specifically, any
        ``frame`` that is composed solely of one or more digits 0-9 is accepted.

        >>> BehaviorFull.validate_frame("-5")
        False
        >>> BehaviorFull.validate_frame("05")
        True
        >>> BehaviorFull.validate_frame("hi5")
        False
        >>> BehaviorFull.validate_frame("50")
        True
        >>> BehaviorFull.validate_frame(" 50 ")
        False

        Args:
            frame: Potential frame number to validate

        Returns: ``True`` if ``frame`` is a valid frame number, ``False``
            otherwise

        """
        return re.fullmatch(r"\A[0-9]+\Z", frame) is not None

    @staticmethod
    def validate_time(time_str: str) -> bool:
        """Check whether ``time_str`` represents a valid log time stamp

        The following formats are accepted where ``#`` represents a digit 0-9
        * ``#:##.##``
        * ``##:##.##``
        * ``#:##:##.##``
        * ``##:##:##.##``

        TODO: Check whether the minute and hour values are valid (i.e. <60)

        Args:
            time_str: The potential time representation to validate

        Returns: ``True`` if ``time_str`` is a valid time, ``False`` otherwise

        """
        num_colons = time_str.count(":")

        if num_colons == 1:
            return re.fullmatch(r"\A[0-9]{1,2}:[0-9]{2}\.[0-9]{2}\Z",
                                time_str) is not None
        if num_colons == 2:
            return re.fullmatch(r"\A[0-9]{1,2}:[0-9]{2}:[0-9]{2}\.[0-9]{2}\Z",
                                time_str) is not None

        return False

    @staticmethod
    def validate_behavior(behavior: str) -> bool:
        """Check whether ``behavior`` is a valid behavior description

        To be valid, ``behavior`` must be made exclusively of digits, letters,
        and spaces.

        >>> BehaviorFull.validate_behavior("Some behavior Description 3!")
        False
        >>> BehaviorFull.validate_behavior("Some behavior Description 3")
        True
        >>> BehaviorFull.validate_behavior("Some behavior Description 3 here")
        True
        >>> BehaviorFull.validate_behavior("Some behavior \\n Description 3!")
        False

        Args:
            behavior: The potential behavior description to check

        Returns: ``True`` if ``behavior`` is valid, ``False`` otherwise

        """
        return re.fullmatch(r"\A[0-9A-Za-z ]+\Z", behavior) is not None

    @staticmethod
    def validate_subject(subject: str) -> bool:
        """Check whether ``subject`` is a valid subject element

        To be valid, ``subject`` must be exactly ``either``

        >>> BehaviorFull.validate_subject("either")
        True
        >>> BehaviorFull.validate_subject(" either")
        False

        Args:
            subject: Potential subject element of a log to check

        Returns: ``True`` if ``subject`` is valid, ``False`` otherwise

        """
        return subject == "either"
