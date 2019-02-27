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

from typing import List
from scorevideo_lib.parse_log import Log, RawLog
from scorevideo_lib.add_marks import copy_mark, get_ending_mark, \
    get_ending_behav
from scorevideo_lib.base_utils import equiv_partition
import os, re


def read_aggr_behav_list():
    with open('fm_behaviors.txt', 'r') as f:
        return [line.rstrip() for line in f]


def copy_lights_on(aggr_logs: List[Log], scored_log: RawLog,
                   aggr_behav_des=List[str]) -> RawLog:
    # For any video i except for the last video, video i+1 starts at the end
    # of video i.
    log_tuples = []
    for log in aggr_logs[:-1]:
        end_mark = get_ending_mark(log.marks)
        s_time = end_mark.time
        s_frame = end_mark.frame
        log_tuples.append((log, s_time, s_frame))
    # For the last video, the next video starts at the first aggressive behavior
    # because only the pre-scoring videos should be in aggr_logs
    last_log = aggr_logs[-1]
    s_behav = get_ending_behav(last_log.full, aggr_behav_des)
    log_tuples.append((last_log, s_behav.time, s_behav.frame))

    return copy_mark(log_tuples, 'LIGHTS ON', scored_log, 'LIGHTS ON')


def get_name_core(filename: str):
    # Discard any file extensions (e.g. .wmv_AA.txt)
    no_extension = os.path.basename(filename).split('.', 1)[0]
    # Discard everything after the last `_` (e.g. 1, 2, or Morning)
    core = no_extension.split('_')[:-1]
    return "_".join(core)


def get_last_name_elem(filename: str):
    # Discard any file extensions (e.g. .wmv_AA.txt)
    no_extension = os.path.basename(filename).split('.', 1)[0]
    # Keep everything after the last `_` (e.g. 1, 2, or Morning)
    end = no_extension.split('_')[-1]
    return end


def same_fish_and_day(name1: str, name2: str):
    return get_name_core(name1) == get_name_core(name2)


def is_scored(filename: str):
    last_elem = get_last_name_elem(filename)
    return last_elem == "Morning" or last_elem == "Afternoon"


def batch_mark_lights_on(path_to_log_dir: str):
    contents = [x for x in os.listdir(path_to_log_dir) if x[0] != '.']
    form = r"\Alog[0-9]{6}_[0-9A-Z]+[0-9]{6}_[0-9A-Z]+_Dyad_[0-9A-Za-z]+.*\Z"
    files = [os.path.join(path_to_log_dir, x) for x in contents
             if re.fullmatch(form, x) is not None]

    partitions = equiv_partition(files, same_fish_and_day)

    for partition in partitions:
        scored = None
        for filename in partition:
            if is_scored(filename):
                assert scored is None
                scored = filename
        assert scored is not None

        log_names = [name for name in partition if name != scored]
        log_names = sorted(log_names, key=lambda x: int(get_last_name_elem(x)))
        logs = []
        for name in log_names:
            with open(name, 'r') as f:
                logs.append(Log.from_file(f))
        with open(scored, 'r') as f:
            scored_raw = RawLog.from_file(f)
            final = copy_lights_on(logs, scored_raw, read_aggr_behav_list())
        with open(scored, 'w') as f:
            lines = final.to_lines()
            for line in lines:
                f.write(line + "\n")


if __name__ == "__main__":
    batch_mark_lights_on(".")
