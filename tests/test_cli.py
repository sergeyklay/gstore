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

import logging
import signal
from unittest import mock

from gstore import cli, client


def test_main_keyboard_interrupt(monkeypatch):
    """Handle Ctrl-C keyboard event and gracefully terminate work."""
    def mock_init(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr('sys.argv', ['gstore', '--token', 'secret'])
    monkeypatch.setattr(client.Client, '__init__', mock_init)

    assert cli.main() == 128 + signal.SIGINT


def test_get_orgs_without_token(monkeypatch):
    """Call with invalid token leads to exit with a status of one."""
    monkeypatch.setattr('sys.argv', ['gstore', '--token', 'secret'])

    with mock.patch.object(logging.Logger, 'info') as mock_logger:
        assert cli.main() == 1

        mock_logger.assert_called_once_with(
            'Getting organizations for user')


def test_resolve_orgs_without_token(monkeypatch):
    """Call with invalid token leads to exit with a status of one."""
    monkeypatch.setattr('sys.argv', [
        'gstore',
        '--token', 'secret',
        '--org', 'Acme'
    ])

    with mock.patch.object(logging.Logger, 'info') as mock_logger:
        assert cli.main() == 1

        mock_logger.assert_called_once_with(
            'Resolve organizations from provided configuration')
