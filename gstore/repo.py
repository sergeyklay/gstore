# Copyright (C) 2020-2024 Serghei Iakovlev <gnu@serghei.pl>
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
from typing import Optional

import git

from .exceptions import parse_git_errors
from .logger import setup_logger
from .models import Organization, Repository


@dataclass
class Context:
    """Class for passing a context to parallel processes."""

    base_path: str
    logger: logging.Logger


# pylint: disable=invalid-name
_proc_ctx: Optional[Context] = None


def clone(repo: Repository, ctx: Context):
    """Clone a repository to the target directory."""
    ctx.logger.info(
        'Clone repository to %s/%s',
        repo.org.login,
        repo.name)
    repo_path = os.path.join(ctx.base_path, repo.org.login, repo.name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, ignore_errors=True)

    git_url = f'git@github.com:{repo.org.login}/{repo.name}.git'

    try:
        git.Repo.clone_from(git_url, repo_path)
    except git.GitCommandError as exception:
        ctx.logger.error('Failed to clone %s/%s', repo.org.login, repo.name)
        for msg in parse_git_errors(exception):
            ctx.logger.error(msg)


def fetch(repo: Repository, ctx: Context):
    """Sync a repository in the target directory."""
    ctx.logger.info('Update %s/%s repository', repo.org.login, repo.name)
    repo_path = os.path.join(ctx.base_path, repo.org.login, repo.name)
    local_repo = git.Repo(repo_path)

    if not local_repo.heads:
        ctx.logger.info(
            'No remote branches for %s/%s, skip fetching',
            repo.org.login,
            repo.name)
        return

    try:
        ctx.logger.debug(
            'Download objects and refs from %s/%s',
            repo.org.login,
            repo.name)
        local_repo.git.fetch(['--prune', '--quiet'])

        ctx.logger.debug(
            'Pulling all branches from %s/%s',
            repo.org.login,
            repo.name)
        local_repo.git.pull(['--all', '--quiet'])
    except git.GitCommandError as exception:
        ctx.logger.error('Failed to update %s/%s', repo.org.login, repo.name)
        for msg in parse_git_errors(exception):
            ctx.logger.error(msg)


def _do_sync(repos: list[Repository]):
    """Perform repos synchronisation. Intended for internal usage."""
    assert _proc_ctx is not None, "Context not initialized in this process"

    ctx = _proc_ctx

    for repo in repos:
        org_path = os.path.join(ctx.base_path, repo.org.login)
        repo_path = os.path.join(org_path, repo.name)
        git_path = os.path.join(repo_path, '.git')

        if os.path.exists(repo_path):
            if os.path.isfile(repo_path):
                ctx.logger.error(
                    'Unable to sync %s. The path %s is a regular file',
                    repo.name,
                    repo_path)
                continue

            if not os.access(repo_path, os.W_OK | os.X_OK):
                ctx.logger.error(
                    'Unable to sync %s. The path %s is not writeable',
                    repo.name,
                    repo_path)
                continue

            # We're going to run a Git command, but weren't inside a
            # local Git repository.
            if not os.path.exists(git_path):
                ctx.logger.debug('Remove wrong formed local repo from %s',
                                 repo_path)
                shutil.rmtree(repo_path, ignore_errors=True)

        if os.path.exists(git_path):
            fetch(repo, ctx)
        else:
            clone(repo, ctx)


def _init_process(verbose=False, quiet=False, base_path=None):
    """Call when new processes start.

    This function is used as a initializer on a per-process basis due
    to 'spawn' process strategy (at least on Windows and macOS).
    """
    assert isinstance(base_path, str) and base_path

    # Setup logger for use within multiprocessing pool
    setup_logger(verbose, quiet)
    logger = logging.getLogger(__name__)
    logger.info('Initializing process')

    # pylint: disable=global-statement
    global _proc_ctx
    _proc_ctx = Context(base_path=base_path, logger=logger)


def sync(org: Organization, repos: list[Repository], base_path: str, **kwargs):
    """Sync repositories for an organization.

    :param Organization org: Organization to sync
    :param list repos: Repository list to sync
    :param string base_path: Base target to sync repositories
    :keyword bool verbose: Enable debug logging
    :keyword bool quiet: Disable info logging
    :keyword int jobs: The number of worker processes to use
    """
    verbose = kwargs.get('verbose') or False
    quiet = kwargs.get('quiet') or False
    requested_jobs = kwargs.get('jobs') or multiprocessing.cpu_count()

    logger = logging.getLogger(__name__)
    logger.info('Sync repos for %s', org.login)

    # Calculate the number of processes to use
    jobs = min(len(repos), requested_jobs)
    if jobs == 0:
        logger.warning("No repositories to sync")
        return

    org_path = os.path.join(base_path, org.login)
    if not os.path.exists(org_path):
        logger.debug('Creating directory %s', org_path)
        os.makedirs(org_path)

    def chunks(tasks: list, n: int):
        """Yield successive n-sized chunks from tasks list."""
        for i in range(0, len(tasks), n):
            yield tasks[i:i + n]

    logger.info('Processes to be spawned: %s', jobs)
    with multiprocessing.Pool(
            processes=jobs,
            initializer=_init_process,
            initargs=(verbose, quiet, base_path)
    ) as pool:
        pool.map(_do_sync, chunks(repos, jobs))
