# Copyright (C) 2020, 2021, 2022, 2023 Serghei Iakovlev <egrep@protonmail.ch>
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

import os
from unittest.mock import MagicMock, call

from git import GitCommandError

from gstore.repo import _do_sync
from gstore.repo import clone, fetch, sync


def test_clone_success(mocker, repository, repo_target, test_context):
    mocker.patch('gstore.repo._ctx', test_context)
    mock_exists = mocker.patch('os.path.exists')
    mock_removedirs = mocker.patch('os.removedirs')
    mock_clone_from = mocker.patch('git.Repo.clone_from')

    mock_exists.return_value = False

    clone(repository, repo_target)

    mock_exists.assert_called_once_with(repo_target)
    mock_removedirs.assert_not_called()
    mock_clone_from.assert_called_once_with(
        f'git@github.com:{repository.org.login}/{repository.name}.git',
        repo_target,
    )
    test_context.logger.info.assert_called_once_with(
        'Clone repository to %s/%s',
        repository.org.login,
        repository.name
    )


def test_clone_failure(mocker, repository, repo_target, test_context):
    mocker.patch('gstore.repo._ctx', test_context)
    mock_exists = mocker.patch('os.path.exists')
    mock_removedirs = mocker.patch('os.removedirs')
    mock_clone_from = mocker.patch('git.Repo.clone_from')

    mock_exists.return_value = True
    mock_clone_from.side_effect = GitCommandError(
        ['git', 'clone'], 1, 'error message')

    clone(repository, repo_target)

    mock_exists.assert_called_once_with(repo_target)
    mock_removedirs.assert_called_once_with(repo_target)
    mock_clone_from.assert_called_once_with(
        f'git@github.com:{repository.org.login}/{repository.name}.git',
        repo_target,
    )
    test_context.logger.error.assert_called()


def test_fetch_success(mocker, repository, repo_target, test_context):
    mocker.patch('gstore.repo._ctx', test_context)
    mock_repo = mocker.patch('git.Repo')
    mock_local_repo = MagicMock()
    mock_repo.return_value = mock_local_repo
    mock_local_repo.heads = ['master']

    fetch(repository, repo_target)

    test_context.logger.info.assert_called_once_with(
        'Update %s/%s repository',
        repository.org.login,
        repository.name
    )
    mock_local_repo.git.fetch.assert_called_once_with(['--prune', '--quiet'])
    mock_local_repo.git.pull.assert_called_once_with(['--all', '--quiet'])


def test_fetch_failure(mocker, repository, repo_target, test_context):
    mocker.patch('gstore.repo._ctx', test_context)
    mock_repo = mocker.patch('git.Repo')
    mock_local_repo = MagicMock()
    mock_repo.return_value = mock_local_repo
    mock_local_repo.heads = ['master']

    mock_local_repo.git.fetch.side_effect = GitCommandError(
        ['git', 'fetch'], 1, 'fetch error message')
    fetch(repository, repo_target)

    test_context.logger.error.assert_called()


def test_do_sync(mocker, repository, repo_target, test_context):
    mocker.patch('gstore.repo._ctx', test_context)
    mock_clone = mocker.patch('gstore.repo.clone')
    mock_fetch = mocker.patch('gstore.repo.fetch')
    repos_list = [repository]

    _do_sync(repos_list)

    org_path = os.path.join(test_context.base_path, repository.org.login)
    repo_path = os.path.join(org_path, repository.name)
    mock_clone.assert_called_once_with(repository, repo_path)
    mock_fetch.assert_not_called()


def test_sync(mocker, organization, repository, repo_target, test_context):
    mocker.patch('gstore.repo._ctx', test_context)
    mocker.patch('multiprocessing.cpu_count', return_value=4)
    mock_pool = MagicMock()
    mock_pool.__enter__.return_value = mock_pool
    mocker.patch('multiprocessing.Pool', return_value=mock_pool)
    mocker.patch('os.makedirs')

    repos = [repository]
    base_path = os.path.dirname(repo_target)

    sync(organization, repos, base_path)

    test_context.logger.info.assert_has_calls(
        [call('Sync repos for %s', organization.login)])
    test_context.logger.debug.assert_called_once_with(
        'Creating directory %s', os.path.join(base_path, organization.login))
    mock_pool.map.assert_called_once()
