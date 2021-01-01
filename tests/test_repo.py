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

from os import environ

import pytest

from gstore.repo import RepoManager

HOME_DIR = environ.get('HOME')

paths_data = [
    ('~/work', '%s/work' % HOME_DIR),
    ('~/backup/~/work', '%s/backup/~/work' % HOME_DIR),
    ('/mnt/backup\\', '/mnt/backup'),
    ('/mnt/backup////', '/mnt/backup'),
    ('/mnt/backup\\//', '/mnt/backup'),
    ('./backup/', './backup'),
    ('c:\\projects\\', 'c:\\projects'),
    ('', ''),
    ('data', 'data'),
]


@pytest.mark.parametrize('actual,expected', paths_data)
def test_repo_manager_init(actual, expected):
    rm = RepoManager(actual)
    assert rm.base_path == expected
