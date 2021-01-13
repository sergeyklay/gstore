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

import signal

from gstore import cli, client


def test_main_keyboard_interrupt(monkeypatch):
    def mock_init(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr('sys.argv', ['gstore', '--token', 'secret'])
    monkeypatch.setattr(client.Client, '__init__', mock_init)

    assert cli.main() == 128 + signal.SIGINT
