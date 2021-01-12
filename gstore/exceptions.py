# Copyright (C) 2020, 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

"""Helper routines and classes to work exceptions.

Classes:

    Error

Functions:

    parse_git_errors() -> list

"""

import re

import git


def parse_git_errors(ex: git.CommandError) -> list:
    """Parse errors produced by :class:`git.GitCommandError` subclasses.

    :param git.GitCommandError ex: An error instance
    :return: A list of error messages
    :rtype: list of str
    """
    def replace(msg):
        """Replace multiline messages to a single-line form."""
        oneliner = re.compile(r'[\s]{2,}|\n')
        cleaner = re.compile(r"(?:(?:std(?:out|err)|error):[ ]*'?)")

        return cleaner.sub('', oneliner.sub(' ', msg)).strip(" .'")

    holders = []

    if ex.stdout:
        holders.append(ex.stdout)
    if ex.stderr:
        holders.append(ex.stderr)

    messages = map(replace, holders)

    return list(messages)


class Error(Exception):
    """Base class for exceptions in gstore module."""
