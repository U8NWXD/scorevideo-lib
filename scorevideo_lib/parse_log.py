# scorevideo_lib: A library for working with scorevideo
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

class Log:

    @staticmethod
    def get_section_header(log_file):
        """Get the header section of a log

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
        """Get the video info section of a log

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
        while log_file.readline().rstrip() != "VIDEO FILE SET":
            pass
        video_info = []
        line = log_file.readline().rstrip()
        while not line == "":
            video_info.append(line)
            line = log_file.readline().rstrip()
        return video_info

    @staticmethod
    def get_section_commands(log_file):
        """Get the commands section of a log

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
        pass

    @staticmethod
    def get_section_raw(log_file):
        """Get the raw log section of a log

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
        pass

    @staticmethod
    def get_section_full(log_file):
        """Get the full log section of a log

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
        pass

    @staticmethod
    def get_section_notes(log_file):
        """Get the notes section of a log

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
        pass

    @staticmethod
    def get_section_marks(log_file):
        """Get the marks section of a log

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
        pass
