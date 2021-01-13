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

import pytest
from github import Github
from github.GithubException import UnknownObjectException

from gstore.client import Client
from gstore.repo import Organization


class MicroMock:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __iter__(self):
        return iter([])


class MockOrganization:
    @staticmethod
    def get_repo(name):
        return MicroMock(name=name)

    @staticmethod
    def get_repos(*args, **kwargs):
        return MicroMock(totalCount=0)


class MockUser:
    login = 'mock_user'

    @staticmethod
    def get_orgs():
        return MicroMock(totalCount=0)


@pytest.fixture
def mock_user(monkeypatch):
    """github.Github.get_user() mocked to return fake user."""
    def mock_get_user(*args, **kwargs):
        return MockUser()

    monkeypatch.setattr(
        Github,
        'get_user',
        mock_get_user
    )


@pytest.fixture
def mock_micro_organization(monkeypatch):
    """github.Github.get_organization() mocked to return fake organization
    object without methods.
    """
    def mock_get_organization(_, name):
        return MicroMock(login=name)

    monkeypatch.setattr(
        Github,
        'get_organization',
        mock_get_organization
    )


@pytest.fixture
def mock_organization(monkeypatch):
    """github.Github.get_organization() mocked to return fake organization."""
    def mock_get_organization(*args, **kwargs):
        return MockOrganization()

    monkeypatch.setattr(
        Github,
        'get_organization',
        mock_get_organization
    )


@pytest.fixture
def mock_orgs_iter(monkeypatch):
    """MicroMock.__iter__() mocked to return fake list of organizations."""
    def mock_iter(*args, **kwargs):
        return iter(
            [MicroMock(login='awesome'), MicroMock(login='company')]
        )

    monkeypatch.setattr(
        MicroMock,
        '__iter__',
        mock_iter
    )


@pytest.fixture
def mock_repos_iter(monkeypatch):
    """MicroMock.__iter__() mocked to return fake list of repositories."""
    def mock_get_repos(*args, **kwargs):
        return iter(
            [MicroMock(name='repo1'), MicroMock(name='repo2')]
        )

    monkeypatch.setattr(
        MicroMock,
        '__iter__',
        mock_get_repos
    )


@pytest.fixture
def mock_repository(monkeypatch):
    """MockOrganization.get_repo() mocked to raise
    github.GithubException.UnknownObjectException.
    """
    def mock_get_repo(*args, **kwargs):
        raise UnknownObjectException(401, 'Not found')

    monkeypatch.setattr(
        MockOrganization,
        'get_repo',
        mock_get_repo
    )


@pytest.fixture
def client():
    """Return a Client instance."""
    return Client('secret')


@pytest.fixture
def organization():
    """Return an Organization instance."""
    return Organization('Acme')
