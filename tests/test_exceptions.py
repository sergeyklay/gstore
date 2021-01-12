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

import git

from gstore import exceptions


def test_parse_git_errors():
    """Call gstore.exceptions.parse_git_errors() will format error message."""

    actual = ("Your configuration specifies to merge with the ref " +
              "'refs/heads/master' from the remote, but no such ref " +
              "was fetched.")

    expected = ("Your configuration specifies to merge with the ref " +
                "'refs/heads/master' from the remote, but no such ref " +
                "was fetched")

    error = git.CommandError('git', stdout=actual)
    assert exceptions.parse_git_errors(error) == [expected]

    error = git.CommandError('git', stderr=actual)
    assert exceptions.parse_git_errors(error) == [expected]

    error = git.CommandError('git', stdout=actual, stderr=actual)
    assert exceptions.parse_git_errors(error) == [expected, expected]

    error = git.CommandError('git')
    assert exceptions.parse_git_errors(error) == []
