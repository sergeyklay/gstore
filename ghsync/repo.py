# Copyright (C) 2020 Serghei Iakovlev <egrep@protonmail.ch>
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

from git import RemoteProgress


class RepoProgressPrinter(RemoteProgress):
    """
    Extended progress printer
    """

    def update(self, op_code, cur_count, max_count=None, message=''):
        print(op_code, cur_count, max_count, cur_count /
              (max_count or 100.0), message or "NO MESSAGE")
