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
from datetime import datetime
from functools import total_ordering
from scorevideo_lib.exceptions import FileFormatError
from scorevideo_lib.base_utils import BaseOps


class Log(BaseOps):
    """Store a parsed version of a log file

    This version stores only the information contained in the log, not any
    information tied to a particular file (e.g. file name, reference to file,
    number of spaces separating columns).

    Attributes:
        full: A list of :py:class:`BehaviorFull` objects, each representing a
            line from the log file's ``FULL`` section
        marks: A list of :py:class:`Mark` objects, each representing a mark from
            the log file

    """
    def __init__(self) -> None:
        """Initialize instance attributes as ``None``

        """
        # self.header = None
        # self.video_info = None
        # self.commands = None
        # self.raw = None
        temp_behav = [BehaviorFull(" 0  00:00.00  null  either ")]
        self.full = temp_behav  # type: List[BehaviorFull]
        # self.notes = None
        self.marks = [Mark(0, timedelta(0), "")]  # type:  List[Mark]

    @classmethod
    def from_log(cls, log: "Log") -> "Log":
        """Create a :py:class:`Log` object from another :py:class:`Log` object

        Args:
            log: The object to copy

        Returns:
            A copy of the ``log`` parameter

        """
        new_log = Log()
        # new_log.header = log.header
        # new_log.video_info = log.video_info
        # new_log.commands = log.commands
        # new_log.raw = log.raw
        new_log.full = log.full.copy()
        # new_log.notes = log.notes
        new_log.marks = log.marks.copy()
        return new_log

    @classmethod
    def from_raw_log(cls, log: "RawLog") -> "Log":
        """Create a :py:class:`Log`` from a :py:class:`RawLog` object

        In the process, the log lines are parsed into their respective objects.
        This process is lossy.

        Args:
            log: The object to parse and to create the object from

        Returns:
            A parsed version of ``log``

        """
        new_log = Log()

        new_log.full = [BehaviorFull(line) for line in log.full]
        new_log.marks = [Mark.from_line(line) for line in log.marks]

        return new_log

    @classmethod
    def from_file(cls, log_file) -> "Log":
        """Create a :py:class:`Log` object from a file

        Args:
            log_file: File to read from

        Returns:
            A parsed representation of ``log_file``

        """
        raw = RawLog.from_file(log_file)
        return cls.from_raw_log(raw)

    def sort_lists(self) -> None:
        """Sort the lists of parsed material as applicable

        Returns:
            None

        """
        self.marks.sort()
        self.full.sort()


class RawLog(BaseOps):
    """Store an interpreted form of a log file and perform operations on it

    Attributes:
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

    def __init__(self) -> None:
        self.header = []  # type: List[str]
        self.video_info = []  # type: List[str]
        self.commands = []  # type: List[str]
        self.raw = []  # type: List[str]
        self.full = []  # type: List[str]
        self.notes = []  # type: List[str]
        self.marks = []  # type: List[str]

    @classmethod
    def from_file(cls, log_file) -> "RawLog":
        """Parse log file into its sections.

        Populate the attributes of the RawLog class by using the get_section_*
        static methods to extract sections that are stored in attributes.

        Args:
            log_file: An open file object that points to the log file to read.
        """

        log = RawLog()

        log.header = RawLog.get_section_header(log_file)
        log.video_info = RawLog.get_section_video_info(log_file)
        log.commands = RawLog.get_section_commands(log_file)
        log.raw = RawLog.get_section_raw(log_file)
        log.full = RawLog.get_section_full(log_file)
        log.notes = RawLog.get_section_notes(log_file)
        log.marks = RawLog.get_section_marks(log_file)
        log_file.seek(0)

        return log

    @classmethod
    def from_raw_log(cls, raw_log: "RawLog") -> "RawLog":
        """Make a copy of a :py:class:`RawLog` object by copying each attribute

        Args:
            raw_log: Object to copy

        Returns:
            Copy of ``raw_log``

        """
        new_log = RawLog()

        new_log.header = raw_log.header
        new_log.video_info = raw_log.video_info
        new_log.commands = raw_log.commands
        new_log.raw = raw_log.raw
        new_log.full = raw_log.full
        new_log.notes = raw_log.notes
        new_log.marks = raw_log.marks

        return new_log

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
        return RawLog.get_section(log_file, "VIDEO FILE SET", [], "")

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
        return RawLog.get_section(log_file, "COMMAND SET AND SETTINGS", header,
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
        return RawLog.get_section(log_file, "RAW LOG", header, end)

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
        return RawLog.get_section(log_file, "FULL LOG", header, end)

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
        return RawLog.get_section(log_file, "NOTES", header, end)

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
        return RawLog.get_section(log_file, "MARKS", header, end)

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


class SectionItem(BaseOps):
    """Superclass for entries in a section of a log

    """

    @staticmethod
    def validate_frame(frame: str) -> bool:
        """Check whether ``frame`` represents a valid frame number

        A valid frame number is any integer. Specifically, any ``frame`` that is
        composed solely of one or more digits 0-9 is accepted. Negative frames
        are allowed and denoted by a prefix of ``-``.

        >>> SectionItem.validate_frame("-5")
        True
        >>> SectionItem.validate_frame("05")
        True
        >>> SectionItem.validate_frame("hi5")
        False
        >>> SectionItem.validate_frame("50")
        True
        >>> SectionItem.validate_frame(" 50 ")
        False

        Args:
            frame: Potential frame number to validate

        Returns: ``True`` if ``frame`` is a valid frame number, ``False``
            otherwise

        """
        if frame[0] == "-":
            frame = frame[1:]

        return re.fullmatch(r"\A[0-9]+\Z", frame) is not None

    @staticmethod
    def validate_time(time_str: str) -> bool:
        """Check whether ``time_str`` represents a valid log time stamp

        The following formats are accepted where ``#`` represents a digit 0-9
        * ``#:##.##``
        * ``##:##.##``
        * ``#:##:##.##``
        * ``##:##:##.##``

        A prefix of ``-`` is also allowed.

        TODO: Check whether the minute and hour values are valid (i.e. <60)

        Args:
            time_str: The potential time representation to validate

        Returns: ``True`` if ``time_str`` is a valid time, ``False`` otherwise

        """
        num_colons = time_str.count(":")

        if time_str[0] == "-":
            time_str = time_str[1:]

        if num_colons == 1:
            return re.fullmatch(r"\A[0-9]{1,2}:[0-9]{2}\.[0-9]{2}\Z",
                                time_str) is not None
        if num_colons == 2:
            return re.fullmatch(r"\A[0-9]{1,2}:[0-9]{2}:[0-9]{2}\.[0-9]{2}\Z",
                                time_str) is not None

        return False

    @staticmethod
    def validate_description(desc: str) -> bool:
        """Check whether ``desc`` is a valid behavior description

        To be valid, ``desc`` must be made exclusively of digits, letters,
        and spaces.

        >>> SectionItem.validate_description("Some Description 3!")
        False
        >>> SectionItem.validate_description("Some Description 3")
        True
        >>> SectionItem.validate_description("Some Description 3 here")
        True
        >>> SectionItem.validate_description("Some \\n Description 3!")
        False

        Args:
            desc: The potential behavior description to check

        Returns: ``True`` if ``desc`` is valid, ``False`` otherwise

        """
        return re.fullmatch(r"\A[0-9A-Za-z ]+\Z", desc) is not None

    @staticmethod
    def split_line(line: str) -> List[str]:
        """Split a RawLog file line in a section into its elements

        Elements must be separated by at least two spaces

        >>> SectionItem.split_line("  hi  4  test   >?why    my4 j   ")
        ['hi', '4', 'test', '>?why', 'my4 j']

        Args:
            line: Line to split

        Returns: A list of the elements in the provided line

        """
        split = re.split(r"\s{2,}", line)
        split[0] = split[0].lstrip()
        split[-1] = split[-1].rstrip()
        return [elem for elem in split if elem != ""]

    @staticmethod
    def str_to_timedelta(time_str: str) -> timedelta:
        """Convert a string representation of a time into a :py:class:timedelta

        >>> SectionItem.str_to_timedelta("30:00.03")
        datetime.timedelta(0, 1800, 30000)

        Args:
            time_str: String representation of the time or duration

        Returns: :py:class:timedelta object that represents the same duration
            or time as ``time_str`` does.

        """
        neg = False

        if time_str[0] == "-":
            neg = True
            time_str = time_str[1:]

        split_time = time_str.split(":")
        secs = float(split_time[-1])
        # MM:SS.SS -> [MM, SS.SS]
        if len(split_time) == 2:
            secs += int(split_time[0]) * 60
        # HH:MM:SS.SS -> [HH, MM, SS.SS]
        elif len(split_time) == 3:
            secs += int(split_time[0]) * 60 * 60
            secs += int(split_time[1]) * 60
        if neg:
            secs = -secs
        return timedelta(seconds=secs)


@total_ordering
class BehaviorFull(SectionItem):
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
        datetime.timedelta(0, 58, 970000)
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
        line = SectionItem.split_line(behavior_line)
        line_error = "The line '" + behavior_line + "' is not a valid line " \
                                                    "from the FULL LOG section"
        if len(line) > 4:
            err = "{} (num elements: {} > 4)".format(line_error, len(line))
            raise TypeError(err)
        elif len(line) < 4:
            err = "{} (num elements: {} < 4)".format(line_error, len(line))
            raise TypeError(err)
        elif not SectionItem.validate_frame(line[0]):
            err = "{} ('{}' is not a valid frame number)".format(line_error,
                                                                 line[0])
            raise TypeError(err)
        elif not SectionItem.validate_time(line[1]):
            err = "{} ('{}' is not a valid time)".format(line_error, line[1])
            raise TypeError(err)
        elif not SectionItem.validate_description(line[2]):
            err = "{} ('{}' is not a valid behavior)".format(line_error,
                                                             line[2])
            raise TypeError(err)
        elif not BehaviorFull.validate_subject(line[3]):
            err = "{} ('{}' is not a valid subject)".format(line_error, line[3])
            raise TypeError(err)

        self.frame = int(line[0])
        self.time = SectionItem.str_to_timedelta(line[1])
        self.description = line[2]
        self.subject = line[3]

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

    def __lt__(self, other: "BehaviorFull"):
        if self.frame != other.frame:
            return self.frame < other.frame
        if self.time != other.time:
            return self.time < other.time
        if self.description != other.description:
            return self.description < other.description
        if self.subject != other.subject:
            return self.subject < other.subject
        return False


@total_ordering
class Mark(SectionItem):
    """Store a ``mark`` from the ``MARKS`` section

    Attributes:
        frame: An integer representing the frame number at which the
            mark is placed
        time: A :py:class:timedelta object that represents the time elapsed
            from the start of the clip to the mark. This is a
            representation of the time listed in the log line. Negative times
            are supported and are represented as their absolute times prefixed
            with a ``-``.
        name: Name of the mark that describes its meaning
    """

    def __init__(self, frame: int, time: timedelta, name: str) -> None:
        self.frame = frame
        self.time = time
        self.name = name

    @classmethod
    def from_line(cls, line: str) -> "Mark":
        """Create a new :py:class:Mark from a provided line from the log file

        >>> mark = Mark.from_line("54001    30:00.03    video end")
        >>> mark.frame
        54001
        >>> mark.time
        datetime.timedelta(0, 1800, 30000)
        >>> mark.name
        'video end'

        Args:
            line: A line from the ``MARKS`` section of a log file
        Returns:
            None
        Raises:
            TypeError: When the provided line does not conform to the
                expected format. Notably, all 3 elements of the line must be
                separated from each other by at least 2 spaces.

        """
        elems = SectionItem.split_line(line)
        line_error = "The line '{}' is not a valid line from the MARKS section"\
            .format(line)
        if len(elems) < 3:
            err = "{} (num elements: {} < 3)".format(line_error, len(elems))
            raise TypeError(err)
        elif len(elems) > 3:
            err = "{} (num elements: {} > 3)".format(line_error, len(elems))
            raise TypeError(err)
        elif not SectionItem.validate_frame(elems[0]):
            err = "{} (frame '{}' is not valid)".format(line_error, elems[0])
            raise TypeError(err)
        elif not SectionItem.validate_time(elems[1]):
            err = "{} (time '{}' is not valid)".format(line_error, elems[1])
            raise TypeError(err)
        elif not SectionItem.validate_description(elems[2]):
            err = "{} (mark name '{}' is invalid)".format(line_error, elems[2])
            raise TypeError(err)

        frame = int(elems[0])
        time = SectionItem.str_to_timedelta(elems[1])
        name = elems[2]

        return cls(frame, time, name)

    def to_line(self, other_line: str) -> str:
        """Converts a :py:class:Mark object into a log line in the MARKS section

        ``other_line`` is used as a template. It should come from the log file
        the returned line will be inserted into. Only loose error checking is
        performed, and invalid lines may produce undefined output. Similarly,
        if the constructed line cannot fit into the format prescribed by
        ``other_line``, the output is undefined.

        >>> mark = Mark(734, timedelta(seconds=1800.07), "video end")
        >>> mark.to_line("  1    0:00.03    video start")
        '734   30:00.07    video end'

        Args:
            other_line: A line from the MARKS section into which the resulting
                string could be inserted. This defines the format this method
                will attempt to match.

        Returns: A log line that could be inserted into the MARKS section of
            the log from which ``other_line`` came.

        Raises:
            ValueError: Raised if ``other_line`` is invalid or the mark's time
                is greater than 1 day

        """
        match = re.search(r"\A(\s*\S+)(\s{2,}\S+)(\s{2,})(?:\S+\s*)+",
                          other_line)
        if match is None:
            err = "other_line '{}' is not a valid line from the MARKS section".\
                format(other_line)
            raise ValueError(err)
        # match.group(n) returns the string in other_line that was matched by
        # the n-th parenthesized group in the regular expression. Note that
        # `(?: ... )` does not count as a group in this context
        frame_col_width = len(match.group(1))
        time_col_width = len(match[2])
        time_name_sep_width = len(match[3])

        time = datetime.utcfromtimestamp(abs(self.time.total_seconds()))
        if abs(self.time) < timedelta(seconds=60):
            # Under 1 minute (all can be expressed in secs microsecs)
            time_str = "0:" + time.strftime("%S.%f")
        elif abs(self.time) < timedelta(seconds=60 * 60):
            # Under 1 hour (all can be expressed in mins, secs, microsecs)
            time_str = time.strftime("%M:%S.%f")
            if time_str[0] == "0":
                time_str = time_str[1:]
        elif abs(self.time) < timedelta(days=1):
            # Under 1 day (all can be expressed in hrs, mins, secs, microsecs)
            time_str = time.strftime("%H:%M:%S.%f")
            if time_str[0] == "0":
                time_str = time_str[1:]
        else:
            raise ValueError("The duration '{}' is too long (must be < 1 day)"
                             .format(str(self.time)))

        # Truncate time_str to cut off all but 2 most significant decimal places
        time_str = time_str[:time_str.index(".") + 3]

        # Add negative sign for negative times
        if self.time.total_seconds() < 0:
            time_str = "-" + time_str

        # Creates a template like "{0:>frame_col_width}{1:>time_col_width}  {2}"
        # Both the frame and time columns are right-justified and of lengths
        # fixed by the variables frame_col_width and time_col_width. 0, 1, and 2
        # are indices that define the locations to fill each arg of .format(...)
        template = "{0:>" + str(frame_col_width) + "}{1:>" + \
                   str(time_col_width) + "}" + (" " * time_name_sep_width) + \
                   "{2}"
        return template.format(self.frame, time_str, self.name)

    def __lt__(self, other: "Mark"):
        """Determine if one :py:class:`Mark` is less than another

        Ordering is performed with the ``<`` operator on the class's attributes
        in the following descending order of priority:
        * :py:attr:`Mark.frame`
        * :py:attr:`Mark.time`
        * :py:attr:`Mark.name`

        Args:
            other: The :py:class:`Mark` to compare to ``self``

        Returns:
            ``True`` if and only if ``self`` comes before ``other``

        """
        if self.frame != other.frame:
            return self.frame < other.frame
        if self.time != other.time:
            return self.time < other.time
        if self.name != other.time:
            return self.name < other.name
        return False
