# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""A tool that adds marks to scored log files based on a ``LIGHTS ON`` behavior

The marks are added with negative time and frame so as to accurately record
when, relative to the start of the scored log file, the lights were recorded
coming on.

When called directly, this script assumes that the log files are present in the
current directory (``.``). Files are partitioned such that each partition holds
the logs for one fish on one day. Afternoon files are ignored, and the
``LIGHTS_ON`` behavior in the ``_1`` or ``_2`` logs is transferred to the
``_Morning`` log.

WARNING: This script is NOT general. It is specific to one particular
    experiment. It may, however, be a useful example for other researchers.

"""

import os
import re
from typing import List
from scorevideo_lib.parse_log import Log, RawLog
from scorevideo_lib.add_marks import copy_mark, get_ending_mark, \
    get_ending_behav
from scorevideo_lib.base_utils import equiv_partition


def read_aggr_behav_list() -> List[str]:
    """Read in the list of FM behaviors that are aggressive / submissive

    Returns: List of behaviors that constitute the start of behavior, trimming
        off trailing whitespace

    """
    with open('fm_behaviors.txt', 'r') as f:
        return [line.rstrip() for line in f]


def copy_lights_on(aggr_logs: List[Log], scored_log: RawLog,
                   aggr_behav_des=List[str]) -> RawLog:
    """Copy a ``LIGHTS ON`` mark from aggression logs to the scored log

    Args:
        aggr_logs: Aggression logs are the ``_1`` or ``_2`` logs in which the
            researcher is looking for the first aggressive or submissive
            behavior by the focal male to begin scoring.
        scored_log: The scored log is the log from the video that was fully
            scored for behaviors.
        aggr_behav_des: List of behavior description sections that indicate that
            a particular behavior is considered aggressive or submissive for
            the purposes of beginning to fully score the video.

    Returns: A copy of ``scored_log``, but with the ``LIGHTS ON`` mark inserted.

    """
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


def get_name_core(filename: str) -> str:
    """Get the core of a filename

    The core is the part of the filename that precedes the identifier that
    separates videos of the same fish on the same day. For example:

    >>> get_name_core("log050118_OB5B030618_TA23_Dyad_Morning.avi_CS")
    'log050118_OB5B030618_TA23_Dyad'

    Args:
        filename: The filename from which to extract the core

    Returns: The core of the filename

    """
    # Discard any file extensions (e.g. .wmv_AA.txt)
    no_extension: str = os.path.basename(filename).split('.', 1)[0]
    # Discard everything after the last `_` (e.g. 1, 2, or Morning)
    core = no_extension.split('_')[:-1]
    return "_".join(core)


def get_last_name_elem(filename: str) -> str:
    """Get the last underscore-delimited element of the name minus extensions

    The last element is the part that distinguishes videos of the same fish on
    the same day. For example:

    >>> get_last_name_elem("log050118_OB5B030618_TA23_Dyad_Morning.avi_CS")
    'Morning'
    >>> get_last_name_elem("log050118_OB5B030618_TA23_Dyad_2.avi_CS")
    '2'

    Args:
        filename: The name from which to get the last element

    Returns: The last element of the file, which distinguishes videos of the
        same fish on the same day

    """
    # Discard any file extensions (e.g. .wmv_AA.txt)
    no_extension: str = os.path.basename(filename).split('.', 1)[0]
    # Keep everything after the last `_` (e.g. 1, 2, or Morning)
    end = no_extension.split('_')[-1]
    return end


def same_fish_and_day(name1: str, name2: str) -> bool:
    """Check whether two files are from the same fish on the same day

    Uses :py:func:`get_name_core` to see whether the names have the same core.

    >>> same_fish_and_day("log050118_OB5B030618_TA23_Dyad_Morning.avi_CS", \
    "log050118_OB5B030618_TA23_Dyad_1.avi_CS")
    True
    >>> same_fish_and_day("log050118_OB5B030618_TA25_Dyad_Morning.avi_CS", \
    "log050118_OB5B030618_TA23_Dyad_1.avi_CS")
    False

    Args:
        name1: One filename to check
        name2: One filename to check

    Returns: Whether the names share a core

    """
    return get_name_core(name1) == get_name_core(name2)


def is_scored(filename: str) -> bool:
    """Check whether a filename is for a full scoring log

    Uses :py:func:`get_last_name_elem` and checks whether the last name element
    is ``Morning`` or ``Afternoon``.

    >>> is_scored("log050118_OB5B030618_TA23_Dyad_Morning.avi_CS")
    True
    >>> is_scored("log050118_OB5B030618_TA23_Dyad_1.avi_CS")
    False

    Args:
        filename: The filename to check

    Returns: Whether the file is for a full scoring log

    """
    last_elem = get_last_name_elem(filename)
    return last_elem in ("Morning", "Afternoon")


def is_lights_on(filename: str) -> bool:
    """Check whether a filename is for a lights-on log

    A lights-on log has the same name as another log, but ends with
    ``_LIGHTSON``. This signals that the ``LIGHTS ON`` behavior in the
    lights-on log should be transferred, maintaining timestamp and frame number,
    to the log of the same name (minus ``_LIGHTSON``, and perhaps different
    scoring initials). Note that the terminal file extension (e.g. ``.txt``) is
    ignored.

    >>> is_lights_on("log050118_OB5B030618_TA23_Dyad_Morning.avi_CS.txt")
    False
    >>> is_lights_on("log050118_OB5B030618_TA23_Dyad_1.avi_CS_LIGHTSON.txt")
    True

    Args:
        filename: Name of log file to check

    Returns:
        Whether the file is a lights-on log
    """
    filename, _ = os.path.splitext(filename)
    terminal = filename.split('_')[-1]
    return terminal == "LIGHTSON"


def batch_mark_lights_on(path_to_log_dir: str) -> None:
    """Transfer ``LIGHTS ON`` marks en masse for all logs in a directory

    The logs are partitioned using :py:func:`same_fish_and_day` into groups of
    logs that pertain to the same fish on the same day. A ``LIGHTS ON`` behavior
    in one of the aggression logs is transferred to the full scoring log,
    accounting for the change in reference point for frame numbers and times.
    The ``LIGHTS ON`` behavior can instead be specified in a separate lights-on
    log (see :py:func:`is_lights_on`). This log should have the same name as the
    log in which the ``LIGHTS ON`` behavior would otherwise be (before being
    transferred), except its name (before the terminal extension like ``.txt``)
    should end in ``_LIGHTSON`` and the initials of the scorer may differ.

    Args:
        path_to_log_dir: Path to the directory of logs to process

    Returns:
        None
    """
    files = [x for x in os.listdir(path_to_log_dir) if x[0] != '.']
    form = r"\Alog[0-9]{6}_[0-9A-Z]+[0-9]{6}_[0-9A-Z]+_Dyad_[0-9A-Za-z]+.*\Z"
    files = [os.path.join(path_to_log_dir, x) for x in files
             if re.fullmatch(form, x) is not None]

    partitions: List[List[str]] = equiv_partition(files, same_fish_and_day)

    for partition in partitions:
        scored = None
        lightson = None
        for filename in partition:
            if is_scored(filename):
                assert scored is None
                scored = filename
            if is_lights_on(filename):
                assert lightson is None
                lightson = filename
        assert scored is not None
        if lightson:
            assert lightson != scored

            with open(lightson, 'r') as f:
                lightson_log = Log.from_file(f)

        log_names = [name for name in partition
                     if name not in (scored, lightson)]
        log_names = sorted(log_names, key=lambda x: int(get_last_name_elem(x)))
        print(log_names)
        logs = []
        for name in log_names:
            with open(name, 'r') as f:
                log = Log.from_file(f)
                if lightson and get_last_name_elem(name) == \
                        get_last_name_elem(lightson):
                    log.extend(lightson_log)
                logs.append(log)
        with open(scored, 'r') as f:
            scored_raw = RawLog.from_file(f)
            final = copy_lights_on(logs, scored_raw, read_aggr_behav_list())
        with open(scored, 'w') as f:
            lines = final.to_lines()
            for line in lines:
                f.write(line + "\n")


if __name__ == "__main__":
    batch_mark_lights_on(".")
