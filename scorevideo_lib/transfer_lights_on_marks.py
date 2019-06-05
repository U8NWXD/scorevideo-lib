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
from typing import List, Tuple, Optional
from scorevideo_lib.parse_log import Log, RawLog
from scorevideo_lib.add_marks import copy_mark, get_ending_mark, \
    get_ending_behav
from scorevideo_lib.base_utils import equiv_partition


class ExpectedFile:
    """Describes the characteristics of a file name for matching

    This is used in :py:const:`PART_REQUIRED` and
    :py:const:`PART_OPTIONAL` to describe required and allowed files.
    """

    def __init__(self, present: List[str] = None, absent: List[str] = None,
                 regex: str = None) -> None:
        """Create a new file description

        Args:
            present: Substrings expected to be present in the file name
            absent: Substrings expected to be absent in the file name
            regex: Regular expression expected to match the file name
        """
        if present:
            self.present = present
        else:
            self.present = []

        if absent:
            self.absent = absent
        else:
            self.absent = []
        self.regex = regex

    def match(self, to_test: str) -> bool:
        """Checks whether a file name matches this description.

        A file matches if it satisfies every specified instance field. For
        example:
        >>> ExpectedFile(['a', 'b'], ['c']).match('ab')
        True
        >>> ExpectedFile(['a', 'b'], ['c']).match('abc')
        False
        >>> ExpectedFile(['a', 'b'], ['c']).match('ac')
        False
        >>> ExpectedFile(['a', 'b'], ['c']).match('a')
        False
        >>> ExpectedFile(['a', 'b'], ['c'], r'[abc]*.txt').match('ab')
        False
        >>> ExpectedFile(['a', 'b'], ['c'], r'[abc]*.txt').match('ab.txt')
        True
        >>> ExpectedFile(['a', 'b'], ['c'], r'[abc]*.txt').match('abc.txt')
        False

        Args:
            to_test: The string to check for matching

        Returns:
            ``True`` if and only if the file name matches.
        """
        for s in self.present:
            if s not in to_test:
                return False
        for s in self.absent:
            if s in to_test:
                return False
        if self.regex and re.fullmatch(self.regex, to_test) is None:
            return False
        return True

    def __repr__(self) -> str:
        return "ExpectedFile[present={}, absent={}, regex={}]".format(
            self.present, self.absent, self.regex)

    def __str__(self) -> str:
        return repr(self)


# Specify regular expressions that identify logs required for every partition
PART_REQUIRED = [ExpectedFile(["_Morning."], ["_LIGHTSON.txt"]),
                 ExpectedFile(["_1."], ["_LIGHTSON.txt"])]
# Specify regular expressions that identify logs optional for every partition
PART_OPTIONAL = [ExpectedFile(["_2."], ["_LIGHTSON.txt"]),
                 ExpectedFile(["_LIGHTSON.txt"])]
# Any files in partitions not matching any of the above throw errors

# # Specify regular expressions that identify logs required for every partition
# PART_REQUIRED = [ExpectedFile(["_Morning."], ["_LIGHTSON.txt"]),
#                  ExpectedFile(["_1."], ["_LIGHTSON.txt"]),
#                  ExpectedFile(["_LIGHTSON.txt"])]
# # Specify regular expressions that identify logs optional for every partition
# PART_OPTIONAL = [ExpectedFile(["_2."], ["_LIGHTSON.txt"]),
#                  ]
# # Any files in partitions not matching any of the above throw errors


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
    try:
        s_behav = get_ending_behav(last_log.full, aggr_behav_des)
    except ValueError as error:
        msg = "No ending behavior in aggression logs {}: {}".format(aggr_logs,
                                                                    error)
        raise ValueError(msg)
    log_tuples.append((last_log, s_behav.time, s_behav.frame))

    return copy_mark(log_tuples, 'LIGHTS ON', scored_log, 'LIGHTS ON')


def get_name_core(filename: str) -> str:
    """Get the core of a filename

    The core is the part of the filename that precedes the identifier that
    separates videos of the same fish on the same day. For example:

    >>> get_name_core("log050118_OB5B030618_TA23_Dyad_Morning.avi_CS")
    'log050118_OB5B030618_TA23_Dyad'
    >>> get_name_core("log050118_OB5B030618_TA23_Dyad_1.avi_CS.txt")
    'log050118_OB5B030618_TA23_Dyad'
    >>> get_name_core("tmp/log050118_OB5B030618_TA23_Dyad_Morning.avi_CS")
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
    >>> same_fish_and_day("050118_OB5B030618_TA23_Dyad_Morning.avi_CS", \
    "log050118_OB5B030618_TA23_Dyad_1.avi_CS")
    True
    >>> same_fish_and_day("log050118_OB5B030618_TA25_Dyad_Morning.avi_CS", \
    "log050118_OB5B030618_TA23_Dyad_1.avi_CS")
    False
    >>> same_fish_and_day("050118_OB5B030618_TA25_Dyad_Morning.avi_CS", \
    "log050118_OB5B030618_TA23_Dyad_1.avi_CS")
    False

    Args:
        name1: One filename to check
        name2: One filename to check

    Returns: Whether the names share a core

    """
    _, name1 = os.path.split(name1)
    _, name2 = os.path.split(name2)
    name1 = normalize_name(name1)
    name2 = normalize_name(name2)
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


def normalize_name(filename: str) -> str:
    """Normalize a filename by adding a prefix ``log`` if not already present

    >>> normalize_name("1.wmv_CS.txt")
    'log1.wmv_CS.txt'
    >>> normalize_name("log1.wmv_CS.txt")
    'log1.wmv_CS.txt'
    >>> normalize_name("logfoo")
    'logfoo'

    Args:
        filename: The filename to normalize

    Returns:
        The normalized filename.
    """
    if len(filename) >= 3 and filename[:3] == "log":
        return filename
    return "log" + filename


def name_filter(filename: str) -> bool:
    """Filter for filenames that should be included for processing

    Includes the numbered log files, and the ``Morning`` log files. Excludes the
    ``Afternoon`` log files.

    >>> name_filter("log050118_OB5B030618_TA23_Dyad_Morning.avi_CS.txt")
    True
    >>> name_filter("log050118_OB5B030618_TA23_Dyad_Afternoon.avi_CS.txt")
    False
    >>> name_filter("log050118_OB5B030618_TA23_Dyad_3.avi_CS.txt")
    True

    The ``log`` prefix is ignored

    >>> name_filter("050118_OB5B030618_TA23_Dyad_Morning.avi_CS.txt")
    True
    >>> name_filter("050118_OB5B030618_TA23_Dyad_Afternoon.avi_CS.txt")
    False
    >>> name_filter("050118_OB5B030618_TA23_Dyad_3.avi_CS.txt")
    True

    Args:
        filename: The filename to check

    Returns:
        Whether the file should be included for analysis
    """
    form = r"\Alog[0-9]{6}_[0-9A-Z]+[0-9]{6}_[0-9A-Z]+_Dyad_([0-9]+|(Morning)).*\Z"
    filename = normalize_name(filename)
    return re.fullmatch(form, filename) is not None


def validate_partition(partition: List[str]) -> List[str]:
    """Validates a partitioning of files

    Ensures that no two files match an element of
    :py:const:`PART_OPTIONAL`, and ensures that exactly one file matches
    each element of :py:const:`PART_REQUIRED`. Also ensures that no files that
    don't match any element of either are present.

    Args:
        partition: The list of file names to validate

    Returns:
        A list of problem descriptions, one for each problem discovered. No
        problems are found if and only if ``[]`` is returned.
    """

    probs = []
    required: List[List[str]] = [[] for _ in PART_REQUIRED]
    optional: List[List[str]] = [[] for _ in PART_OPTIONAL]

    for name in partition:
        matched = []
        for i, req in enumerate(PART_REQUIRED):
            if req.match(name):
                matched.append(PART_REQUIRED[i])
                required[i].append(name)
        for i, opt in enumerate(PART_OPTIONAL):
            if opt.match(name):
                matched.append(PART_OPTIONAL[i])
                optional[i].append(name)
        if len(matched) > 1:
            probs.append("File {} matched multiple expectations: {}".
                         format(name, matched))

    for i, files in enumerate(required):
        if not files:
            probs.append("No file found that matches: {}".
                         format(PART_REQUIRED[i]))
        if len(files) > 1:
            probs.append("{} matched multiple files: {}".format(
                PART_REQUIRED[i], files))
    for i, files in enumerate(optional):
        if len(files) > 1:
            probs.append("{} matched multiple files: {}".format(
                PART_REQUIRED[i], files))
    return probs


def find_scored_lights(partition: List[str]) -> \
        Tuple[str, Optional[str]]:
    """Find the full scoring and lights-on log of a partition

    Full scoring logs are identified by :py:func:`is_scored`, and lights-on
    logs are identified by :py:func:`is_lights_on`.

    Args:
        partition: The list of file names from which to identify lights-on
            and full scoring logs.

    Returns:
        Tuple of file names of full scoring log and lights-on log. If no lights
        on log is found, ``None`` is returned instead.

    Raises:
        ValueError: If duplicate full scoring logs or lights-on logs are found,
            if no full scoring log is found, or if the scoring log is the same
            as the lights-on log.
    """
    scored = None
    lightson: Optional[str] = None

    for filename in partition:
        if is_scored(filename):
            if scored is not None:
                msg = "Duplicate full scoring log: {}".format(scored)
                raise ValueError(msg)
            scored = filename
        if is_lights_on(filename):
            if lightson is not None:
                msg = "Duplicate lights-on log: {}".format(lightson)
                raise ValueError(msg)
            lightson = filename
    if scored is None:
        msg = "No full scoring log found for {}".format(partition)
        raise ValueError(msg)
    if lightson:
        if lightson == scored:
            msg = "Lights-on log {} same as the full scoring log {}".format(
                lightson, scored)
            raise ValueError(msg)
    return scored, lightson


def get_partitions(path_to_log_dir: str):
    """Get partitioned file names from the specified directory

    Files beginning with ``.`` are filtered out, as are any files for which
    :py:func:`name_filter` returns ``False``. Names are partitioned using
    :py:func:`equiv_partition`, where equivalence is determined by
    :py:func:`same_fish_and_day` returning ``True``. Each name includes
    the provided path as a prefix. Partitions are validated using
    :py:func:`validate_partition`.

    Args:
        path_to_log_dir: Path to the directory containing log files to partition

    Returns:
        A valid partitioning of the file names.

    Raises:
        ValueError: If any of the partitions fail validation
    """
    files = [x for x in os.listdir(path_to_log_dir) if x[0] != '.']
    files = [os.path.join(path_to_log_dir, x) for x in files
             if name_filter(x)]

    partitions: List[List[str]] = equiv_partition(files, same_fish_and_day)

    probs = False
    for partition in partitions:
        part_probs = validate_partition(partition)
        if part_probs:
            probs = True
            print("Problems with partition: {}".format(partition))
            for prob in part_probs:
                print("\t{}".format(prob))
    if probs:
        raise ValueError("Some partitions are invalid.")

    return partitions


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
    partitions = get_partitions(path_to_log_dir)
    for partition in partitions:
        scored, lightson = find_scored_lights(partition)

        if lightson:
            with open(lightson, 'r') as f:
                lightson_log = Log.from_file(f)

        log_names = [name for name in partition
                     if name not in (scored, lightson)]
        log_names = sorted(log_names, key=lambda x: int(get_last_name_elem(x)))

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
    batch_mark_lights_on("work")
