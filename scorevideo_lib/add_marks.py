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

"""Add marks from annotations (behaviors) in other logs

"""

from typing import List
import re
from datetime import timedelta
from scorevideo_lib.parse_log import RawLog, Log, Mark


START_MARK = "video start"
END_MARK = "video end"


def copy_mark(logs: List[Log], src_pattern: str, dest: RawLog, dest_label) \
        -> RawLog:
    """Copy a behavior into another log file as a mark, adjusting time and frame

    Time and frame are adjusted so as to be correct (potentially by being
    negative) in relation to the other entries in ``dest``, assuming that the
    logs in ``logs`` are in order, consecutive, and non-overlapping and that
    ``dest`` begins immediately after the last behavior scored in the last log
    of ``logs``.

    Args:
        logs: List of consecutive and non-overlapping logs to search for
            ``src_pattern`` in and account for when adjusting time and frame
        src_pattern: Search pattern (regular expression) that identifies
        dest: Log to insert mark into
        dest_label: Label for inserted mark

    Returns:
        A copy of ``dest``, but with the new mark inserted

    """
    found = False
    frames = 0
    time = timedelta(seconds=0)
    for log in logs:
        log.sort_lists()

    for log in logs[:-1]:
        end_mark = get_ending_mark(log.marks)
        if not found:
            for behav in log.full:
                if re.match(src_pattern, behav.description):
                    found = True

                    end_frame = end_mark.frame
                    end_time = end_mark.time

                    frames = end_frame - behav.frame
                    time = end_time - behav.time
        else:
            frames += end_mark.frame
            time += end_mark.time

    last_behavior = logs[-1].full[-1]
    frames += last_behavior.frame
    time += last_behavior.time

    new_mark = Mark(-frames, -time, dest_label)
    new_log = RawLog.from_raw_log(dest)
    new_log.marks.append(new_mark.to_line(new_log.marks[0]))
    return new_log


def get_ending_mark(marks: List[Mark]) -> Mark:
    """Get the mark that has :py:const:`END_MARK` as its :py:attr:`Mark.name`

    Args:
        marks: List of marks to search through

    Returns:
        The identified :py:class:`Mark`

    Raises:
        ValueError: When no matching mark is found

    """
    for mark in marks:
        if mark.name == END_MARK:
            return mark
    raise ValueError("No mark with name '{}' found in list '{}'".format(
        END_MARK, marks))
