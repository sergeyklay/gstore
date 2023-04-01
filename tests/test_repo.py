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

from git import GitCommandError

from gstore.repo import clone


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
