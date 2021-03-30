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
from itertools import zip_longest

import git

from .exceptions import parse_git_errors
from .logger import setup_logger
from .models import Organization, Repository


class Context():
    pass


# Will be used as context in parallel processes
_ctx = Context()
_ctx.logger = None


def clone(repo: Repository, target: str):
    """Clone a repository to the target directory."""
    if _ctx.logger is None:
        _ctx.logger = logging.getLogger('gstore.repo_manager')

    _ctx.logger.info(
        'Clone repository to %s/%s',
        repo.org.login,
        repo.name
    )

    if os.path.exists(target):
        os.removedirs(target)

    git_url = 'git@github.com:%s/%s.git' % (repo.org.login, repo.name)

    try:
        git.Repo.clone_from(
            git_url,
            target,
        )
    except git.GitCommandError as exception:
        _ctx.logger.error(
            'Failed to clone %s/%s',
            repo.org.login,
            repo.name
        )
        for msg in parse_git_errors(exception):
            _ctx.logger.error(msg)


def fetch(repo: Repository, target: str):
    """Sync a repository in the target directory."""
    if _ctx.logger is None:
        _ctx.logger = logging.getLogger('gstore.repo_manager')

    _ctx.logger.info(
        'Update %s/%s repository',
        repo.org.login,
        repo.name
    )
    local_repo = git.Repo(target)

    if len(local_repo.heads) == 0:
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
        _ctx.logger.error(
            'Failed to update %s/%s',
            repo.org.login,
            repo.name
        )
        for msg in parse_git_errors(exception):
            _ctx.logger.error(msg)


def do_sync(params: tuple):
    """Perform repos synchronisation. Intended for internal usage."""
    repos_list, ctx = params  # type: list, Context
    base_path = getattr(ctx, 'base_path')

    setup_logger(
        getattr(ctx, 'verbose', False),
        getattr(ctx, 'quiet', False),
    )

    ctx.logger = logging.getLogger('gstore.repo_manager')

    for repo in repos_list:
        org_path = os.path.join(base_path, repo.org.login)
        repo_path = os.path.join(org_path, repo.name)
        git_path = os.path.join(repo_path, '.git')

        if os.path.exists(repo_path):
            if os.path.isfile(repo_path):
                ctx.logger.error(
                    'Unable to sync %s. The path %s is a regular file',
                    repo.name,
                    repo_path,
                )
                continue

            if not os.access(repo_path, os.W_OK | os.X_OK):
                ctx.logger.error(
                    'Unable to sync %s. The path %s is not writeable',
                    repo.name,
                    repo_path,
                )
                continue

            # We're going to run a Git command, but weren't inside a
            # local Git repository.
            if not os.path.exists(git_path):
                ctx.logger.debug(
                    'Remove wrong formed local repo from %s',
                    repo_path
                )
                shutil.rmtree(repo_path, ignore_errors=True)

        if os.path.exists(git_path):
            fetch(repo, repo_path)
        else:
            clone(repo, repo_path)


def sync(org: Organization, repos: list, base_path: str, ctx=None):
    """Sync repositories for an organization."""
    if _ctx.logger is None:
        _ctx.logger = logging.getLogger('gstore.repo_manager')

    _ctx.logger.info('Sync repos for %s', org.login)

    org_path = os.path.join(base_path, org.login)

    # Just in case create directories recursively
    if not os.path.exists(org_path):
        _ctx.logger.debug('Creating directory %s', org_path)
        os.makedirs(org_path)

    num_proc = multiprocessing.cpu_count()

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    if ctx is None:
        ctx = {}

    _ctx.verbose = ctx.get('verbose', False)
    _ctx.quiet = ctx.get('quiet', False)
    _ctx.base_path = base_path

    tasks = zip_longest(chunks(repos, num_proc), [], fillvalue=_ctx)

    with multiprocessing.Pool(processes=num_proc) as pool:
        pool.map(do_sync, tasks)
