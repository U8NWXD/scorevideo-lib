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
        header = []
        for _ in range(2):
            header.append(log_file.readline())
        return header

    @staticmethod
    def get_section_video_info(log_file):
        while log_file.readline() != "VIDEO FILE SET\n":
            pass
        video_info = []
        line = log_file.readline()
        while not line.rstrip() == "":
            video_info.append(line)
            line = log_file.readline()
        return video_info

    @staticmethod
    def get_section_commands(log_file):
        pass

    @staticmethod
    def get_section_raw(log_file):
        pass

    @staticmethod
    def get_section_full(log_file):
        pass

    @staticmethod
    def get_section_notes(log_file):
        pass

    @staticmethod
    def get_section_marks(log_file):
        pass
