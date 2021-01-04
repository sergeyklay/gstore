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
from github.GithubException import UnknownObjectException

from gstore.client import Client
from gstore.exceptions import InvalidCredentialsError
from gstore.models import Organization, Repository


@pytest.mark.parametrize('token', ['', None, False])
def test_empty_token(token):
    """Call Client() with empty token should raise exception."""
    with pytest.raises(
            InvalidCredentialsError,
            match='GitHub token is not provided or it is empty'):
        Client(token)


def test_resolve_orgs_empty_list():
    """Call Client.resolve_orgs() with empty list should return empty list."""
    client = Client('secret')

    with mock.patch.object(client.logger, 'info') as mock_logger:
        orgs = client.resolve_orgs([])

        assert len(orgs) == 0
        mock_logger.assert_called_once_with(
            'Resolve organizations from provided configuration')


def test_resolve_orgs_unknown_org(monkeypatch):
    """
    Call Client.resolve_orgs() for a non existent organization will not stop
    work but we'll see an error in the logs.
    """
    def mock_get_organization(_):
        raise UnknownObjectException(401, 'Not found')

    client = Client('secret')

    monkeypatch.setattr(
        client.github,
        'get_organization',
        mock_get_organization
    )

    with mock.patch.object(client.logger, 'error') as mock_logger:
        orgs = client.resolve_orgs(['foo-bar-baz'])

        assert len(orgs) == 0
        mock_logger.assert_called_once_with(
            'Invalid organization name "%s"', 'foo-bar-baz')


def test_resolve_orgs(mock_micro_organization):
    """
    Call Client.resolve_orgs() with a non empty list of organization names
    will return a list of :class:`gstore.models.Organization`
    """
    client = Client('secret')

    orgs = client.resolve_orgs(['awesome', 'company'])

    assert len(orgs) == 2
    assert isinstance(orgs[0], Organization)
    assert isinstance(orgs[1], Organization)
    assert orgs[0].login == 'awesome'
    assert orgs[1].login == 'company'


def test_resolve_orgs_invalid_token():
    """Call Client.resolve_orgs() with invalid token."""
    client = Client('secret')

    with pytest.raises(
            InvalidCredentialsError,
            match='Bad token was used when accessing the GitHub API'):
        client.resolve_orgs(['github'])


def test_resolve_repos_empty_list():
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


def test_get_orgs_empty_list(mock_user):
    """
    Call Client.get_orgs() for a user without organizations will return an
    empty list.
    """
    client = Client('secret')

    with mock.patch.object(client.logger, 'info') as mock_logger:
        orgs = client.get_orgs()
        assert len(orgs) == 0

        calls = [
            mock.call('Getting organizations for user'),
            mock.call(
                'Number of available organizations for %s user: %s',
                'mock_user',
                0
            ),
        ]

        mock_logger.assert_has_calls(calls)


def test_get_orgs(mock_user, mock_orgs_iter):
    """
    Call Client.get_orgs() for a user will return a list of
    :class:`gstore.models.Organization`
    """
    client = Client('secret')
    orgs = client.get_orgs()

    assert len(orgs) == 2
    assert isinstance(orgs[0], Organization)
    assert isinstance(orgs[1], Organization)
    assert orgs[0].login == 'awesome'
    assert orgs[1].login == 'company'


def test_resolve_repos_unknown_org(mock_organization, mock_repository):
    """
    Call Client.resolve_repos() for a non existent repository will not stop
    work but we'll see an error in the logs.
    """
    client = Client('secret')

    with mock.patch.object(client.logger, 'error') as mock_logger:
        repos = client.resolve_repos(
            ['Acme:secret-repo'],
            Organization('Acme')
        )

        assert len(repos) == 0
        mock_logger.assert_called_once_with(
            'Invalid repository name "%s"', 'secret-repo')


def test_resolve_repos(mock_organization):
    """
    Call Client.resolve_orgs() with a non empty list of repo patterns
    will return a list of :class:`gstore.models.Repository`
    """
    org = Organization('Acme')
    client = Client('secret')

    repos = client.resolve_repos(['Acme:awesome', 'Acme:repo'], org)

    assert len(repos) == 2
    assert isinstance(repos[0], Repository)
    assert isinstance(repos[1], Repository)
    assert repos[0].name == 'awesome'
    assert repos[1].name == 'repo'


def test_resolve_repos_invalid_token():
    """Call Client.resolve_repos() with invalid token."""
    client = Client('secret')

    with pytest.raises(
            InvalidCredentialsError,
            match='Bad token was used when accessing the GitHub API'):
        client.resolve_repos(['Acme:github'], Organization('Acme'))


@pytest.mark.parametrize('repo', ['', ':', 'a', 'a:', 'a:b:', 'a:b:c'])
def test_resolve_repos_invalid_repo_pattern(repo):
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


def test_get_repos_empty_list(mock_organization):
    """
    Call Client.get_repos() for a organization without repositories will return
    an empty list.
    """
    client = Client('secret')

    with mock.patch.object(client.logger, 'info') as mock_logger:
        repos = client.get_repos(Organization('awesome'))
        assert len(repos) == 0

        calls = [
            mock.call('Getting repositories for organization'),
            mock.call(
                'Number of available repositories for %s organization: %s',
                'awesome',
                0
            ),
        ]

        mock_logger.assert_has_calls(calls)


def test_get_repos(mock_organization, mock_repos_iter):
    """
    Call Client.get_repos() for an organization will return a list of
    :class:`gstore.models.Repository`
    """
    client = Client('secret')
    repos = client.get_repos(Organization('awesome'))

    assert len(repos) == 2
    assert isinstance(repos[0], Repository)
    assert isinstance(repos[1], Repository)
    assert repos[0].name == 'repo1'
    assert repos[1].name == 'repo2'
