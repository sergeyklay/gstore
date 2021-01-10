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

import sys
from argparse import ArgumentParser, Namespace
from unittest import mock

from gstore import args
from gstore import env


def test_none_args(monkeypatch):
    """Show help message and return None if gstore was called without any
    argument and environment variables were not enough to start gstore.
    """
    def mock_lookup_token():
        return None

    monkeypatch.setattr('sys.argv', ['gstore'])
    monkeypatch.setattr(
        env,
        'lookup_token',
        mock_lookup_token
    )

    with mock.patch.object(ArgumentParser, 'print_help') as mock_help:
        assert args.argparse() is None
        mock_help.assert_called_once_with(sys.stderr)


def test_only_token(monkeypatch):
    """Token is enough to run gstore without arguments."""
    def mock_lookup_token():
        return 'secret'

    monkeypatch.setattr('sys.argv', ['gstore'])
    monkeypatch.setattr(
        env,
        'lookup_token',
        mock_lookup_token
    )

    assert isinstance(args.argparse(), Namespace)
