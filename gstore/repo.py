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

"""Repository classes used to wrap git classes for gstore."""

import logging
import multiprocessing
import os
import shutil
from dataclasses import dataclass

import git

from .exceptions import parse_git_errors
from .logger import setup_logger
from .models import Organization, Repository


@dataclass
class _Context:
    """Class for passing a context to parallel processes."""

    base_path: str = ''
    logger: logging.Logger = None


# pylint: disable=invalid-name
_ctx = _Context(
    logger=logging.getLogger(f'{__name__}'),
)


def clone(repo: Repository, target: str):
    """Clone a repository to the target directory."""
    _ctx.logger.info(
        'Clone repository to %s/%s',
        repo.org.login,
        repo.name
    )

    if os.path.exists(target):
        os.removedirs(target)

    git_url = f'git@github.com:{repo.org.login}/{repo.name}.git'

    try:
        git.Repo.clone_from(
            git_url,
            target,
        )
    except git.GitCommandError as exception:
        _ctx.logger.error(f'Failed to clone {repo.org.login}/{repo.name}')
        for msg in parse_git_errors(exception):
            _ctx.logger.error(msg)


def fetch(repo: Repository, target: str):
    """Sync a repository in the target directory."""
    _ctx.logger.info(f'Update {repo.org.login}/{repo.name} repository')
    local_repo = git.Repo(target)

    if not local_repo.heads:
        _ctx.logger.info(
            'There are no remote branches for %s/%s, skip updating',
            repo.org.login,
            repo.name
        )
        return

    try:
        _ctx.logger.debug(
            'Download objects and refs from %s/%s repository',
            repo.org.login,
            repo.name
        )
        local_repo.git.fetch(['--prune', '--quiet'])

        _ctx.logger.debug(
            'Fetch from and integrate with %s/%s repository',
            repo.org.login,
            repo.name
        )
        local_repo.git.pull(['--all', '--quiet'])
    except git.GitCommandError as exception:
        _ctx.logger.error(f'Failed to update {repo.org.login}/{repo.name}')
        for msg in parse_git_errors(exception):
            _ctx.logger.error(msg)


def _do_sync(repos_list):
    """Perform repos synchronisation. Intended for internal usage."""
    assert isinstance(_ctx.base_path, str) and _ctx.base_path

    for repo in repos_list:
        org_path = os.path.join(_ctx.base_path, repo.org.login)
        repo_path = os.path.join(org_path, repo.name)
        git_path = os.path.join(repo_path, '.git')

        if os.path.exists(repo_path):
            if os.path.isfile(repo_path):
                _ctx.logger.error(
                    'Unable to sync %s. The path %s is a regular file',
                    repo.name,
                    repo_path,
                )
                continue

            if not os.access(repo_path, os.W_OK | os.X_OK):
                _ctx.logger.error(
                    'Unable to sync %s. The path %s is not writeable',
                    repo.name,
                    repo_path,
                )
                continue

            # We're going to run a Git command, but weren't inside a
            # local Git repository.
            if not os.path.exists(git_path):
                _ctx.logger.debug(
                    f'Remove wrong formed local repo from {repo_path}'
                )
                shutil.rmtree(repo_path, ignore_errors=True)

        if os.path.exists(git_path):
            fetch(repo, repo_path)
        else:
            clone(repo, repo_path)


def _init_process(verbose=False, quiet=False, base_path=None):
    """Call when new processes start.

    This function is used as a initializer on a per-process basis due
    to 'spawn' process strategy (at least on Windows and macOs).
    """
    assert isinstance(base_path, str) and base_path

    # Setup logger for use within multiprocessing pool
    setup_logger(verbose, quiet)

    # Setup git base path for use within multiprocessing pool
    _ctx.base_path = base_path

    _ctx.logger = logging.getLogger(f'{__name__}')
    _ctx.logger.info('Initializing process')


def sync(org: Organization, repos: list, base_path: str, **kwargs):
    """
    Sync repositories for an organization.

    :param Organization org: Organization to sync
    :param list repos: Repository list to sync
    :param string base_path: Base target to sync repos
    :keyword bool verbose: Enable debug logging
    :keyword bool quiet: Disable info logging
    :keyword int jobs: the number of worker processes to use
    """
    _ctx.logger.info(f'Sync repos for {org.login}')

    org_path = os.path.join(base_path, org.login)

    # Just in case create directories recursively
    if not os.path.exists(org_path):
        _ctx.logger.debug(f'Creating directory {org_path}')
        os.makedirs(org_path)

    jobs = kwargs.get('jobs')
    if not jobs:
        jobs = multiprocessing.cpu_count()

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    _ctx.logger.info(f'Processes to be spawned: {jobs}')
    with multiprocessing.Pool(processes=jobs, initializer=_init_process,
                              initargs=(kwargs.get('verbose', False),
                                        kwargs.get('quiet', False),
                                        base_path)) as pool:
        pool.map(_do_sync, chunks(repos, jobs))
