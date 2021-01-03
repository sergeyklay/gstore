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
from unittest import mock

from gstore.client import Client
from gstore.models import Organization

import pytest


def test_client_resolve_orgs():
    client = Client('secret')

    with mock.patch.object(client.logger, 'info') as mock_logger:
        orgs = client.resolve_orgs([])

        assert len(orgs) == 0
        mock_logger.assert_called_once_with(
            'Resolve organizations from provided configuration')


def test_client_resolve_empty_repos():
    client = Client('secret')
    fake_org = Organization('fake_org')

    with mock.patch.object(client.logger, 'info') as mock_logger:
        repos = client.resolve_repos([], fake_org)

        assert len(repos) == 0
        mock_logger.assert_called_once_with(
            'Resolve repositories from provided configuration')

    repos = client.resolve_repos(['foo:bar'], fake_org)
    assert len(repos) == 0


@pytest.mark.parametrize('repo', ['', ':', 'a', 'a:', 'a:b:', 'a:b:c'])
def test_client_resolve_invalid_repos(repo):
    client = Client('secret')
    fake_org = Organization('fake_org')

    with mock.patch.object(client.logger, 'error') as mock_logger:
        repos = client.resolve_repos([repo], fake_org)

        assert len(repos) == 0
        mock_logger.assert_called_once_with(
            'Invalid repo pattern: "%s", skip resolving', repo)
