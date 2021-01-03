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

from pathlib import Path

import pytest

from gstore.repo import RepoManager


@pytest.mark.parametrize(
    'provided,expected',
    [
        ('~/work', f'''{Path.home()}/work'''),
        ('~/backup/~/work', f'''{Path.home()}/backup/~/work'''),
        ('/mnt/backup\\', '/mnt/backup'),
        ('/mnt/backup////', '/mnt/backup'),
        ('/mnt/backup\\//', '/mnt/backup'),
        ('./backup/', './backup'),
        ('.\\here', '.\\here'),
        ('c:\\projects\\', 'c:\\projects'),
        ('', ''),
        ('data', 'data'),
    ]
)
def test_init(provided, expected):
    """RepoManager() will resolve a base path."""
    manager = RepoManager(provided)
    assert manager.base_path == expected
