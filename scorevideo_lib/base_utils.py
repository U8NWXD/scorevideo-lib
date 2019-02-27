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

from typing import Callable, Iterable, List, Any

"""Basic utilities for generally applicable functions

"""


class BaseOps:
    """Superclass for basic operations

    """

    def __repr__(self):
        # pylint: disable=missing-docstring
        return str(self.__dict__)

    def __str__(self):
        # pylint: disable=missing-docstring
        return self.__repr__()

    def __eq__(self, other):
        # pylint: disable=missing-docstring
        return self.__repr__() == other.__repr__()


def remove_trailing_newline(s: str):
    if len(s) > 0 and s[-1] == "\n":
        s = s[:-1]
    return s
