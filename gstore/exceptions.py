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

"""Exception classes raised by various operations within gstore."""

import re
import git


def parse_git_errors(ex: git.GitCommandError) -> list:
    """
    A helper function to parse errors produced by :class:`git.GitCommandError`
    subclasses.

    :param git.GitCommandError ex: An error instance
    :return: A list of error messages
    :rtype: list of str
    """
    def replace(msg):
        wrp_regex = re.compile(r"(?:(?:std(?:out|err)|error):[ ]*'?|\n)")
        spc_regex = re.compile(r'[\s]{2,}')
        return spc_regex.sub(' ', wrp_regex.sub('', msg)).strip(" .'")

    holders = []

    if ex.stdout:
        holders.append(ex.stdout)
    if ex.stderr:
        holders.append(ex.stderr)

    messages = map(replace, holders)

    return list(messages)


class BaseValidationError(ValueError):
    """Base validation error."""


class InvalidCredentialsError(BaseValidationError):
    """An error resulting from the use of incorrect credentials."""
