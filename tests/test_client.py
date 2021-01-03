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

from unittest import mock

import pytest

from gstore.client import Client
from gstore.models import Organization


@pytest.mark.parametrize('token', ['', None, False])
def test_empty_token(token):
    """Call Client() with empty token should raise exception."""
    with pytest.raises(
            ValueError,
            match='GitHub token is not provided or it is empty'):
        Client(token)


def test_resolve_orgs():
    """Call Client.resolve_orgs() with empty list should return empty list."""
    client = Client('secret')

    with mock.patch.object(client.logger, 'info') as mock_logger:
        orgs = client.resolve_orgs([])

        assert len(orgs) == 0
        mock_logger.assert_called_once_with(
            'Resolve organizations from provided configuration')


def test_resolve_orgs_invalid_token():
    """Call Client.resolve_orgs() with invalid token."""
    client = Client('secret')

    with pytest.raises(
            RuntimeError,
            match='Bad token was used when accessing the GitHub API'):
        client.resolve_orgs(['github'])


def test_resolve_empty_repos():
    """
    Call Client.resolve_repos() with empty repo list or not expected org
    should return empty list.
    """
    client = Client('secret')
    fake_org = Organization('fake_org')

    with mock.patch.object(client.logger, 'info') as mock_logger:
        repos = client.resolve_repos([], fake_org)
        assert len(repos) == 0

        repos = client.resolve_repos(['foo:bar'], fake_org)
        assert len(repos) == 0

        mock_logger.assert_called_with(
            'Resolve repositories from provided configuration'
        )


@pytest.mark.parametrize('repo', ['', ':', 'a', 'a:', 'a:b:', 'a:b:c'])
def test_resolve_invalid_repos(repo):
    """
    Call Client.resolve_repos() with invalid repo pattern
    should return empty list and log error.
    """
    client = Client('secret')
    fake_org = Organization('fake_org')

    with mock.patch.object(client.logger, 'error') as mock_logger:
        repos = client.resolve_repos([repo], fake_org)

        assert len(repos) == 0
        mock_logger.assert_called_once_with(
            'Invalid repo pattern: "%s", skip resolving', repo)
