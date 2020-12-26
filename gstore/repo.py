# Copyright (C) 2020 Serghei Iakovlev <egrep@protonmail.ch>
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
import logging

from git import GitCommandError, Repo, RemoteProgress

LOG = logging.getLogger('gstore.repo')


class RepoProgressPrinter(RemoteProgress):
    """
    Extended progress printer.
    """

    def update(self, op_code, cur_count, max_count=None, message=''):
        """Called whenever the progress changes

        :param op_code:
            Integer allowing to be compared against Operation IDs and stage
            IDs.

            Stage IDs are BEGIN and END. BEGIN will only be set once for each
            Operation ID as well as END. It may be that BEGIN and END are set
            at once in case only one progress message was emitted due to the
            speed of the operation. Between BEGIN and END, none of these flags
            will be set

            Operation IDs are all held within the OP_MASK. Only one Operation
            ID will be active per call.
        :param cur_count: Current absolute count of items

        :param max_count:
            The maximum count of items we expect. It may be None in case there
            is no maximum number of items or if it is (yet) unknown.

        :param message:
            In case of the 'WRITING' operation, it contains the amount of bytes
            transferred. It may, possibly be used for other purposes as well.
        """
        LOG.debug('{} {} {} {} {}'.format(
            op_code,
            cur_count,
            max_count,
            cur_count / (max_count or 100.0),
            message or '',
        ))


def clone(repo_name, org, target):
    LOG.info("Repository %s/%s doesn't exist. Clone ..." % (org, repo_name))

    if os.path.exists(target):
        os.removedirs(target)

    git_url = 'git@github.com:{}/{}.git'.format(org, repo_name)

    try:
        Repo.clone_from(git_url, target, progress=RepoProgressPrinter())
    except GitCommandError as e:
        if e.stdout:
            LOG.critical(e.stdout)
        if e.stderr:
            LOG.critical(e.stderr)


def fetch(repo_name, org, target):
    LOG.info('Repository %s/%s already exist. Sync ...' % (org, repo_name))

    repo = Repo(target)

    try:
        repo.git.fetch(['--prune', '--quiet'])
        repo.git.pull(['--all', '--quiet'])
    except GitCommandError as e:
        if e.stdout:
            LOG.critical(e.stdout)
        if e.stderr:
            LOG.critical(e.stderr)


def do_sync(org, repos, target):
    LOG.info('Sync repos for %s' % org)

    org_path = os.path.join(target, org)

    # Just in case create directories recursively
    if not os.path.exists(org_path):
        os.makedirs(org_path)

    for repo_name in repos:
        repo_path = os.path.join(org_path, repo_name)

        if os.path.isfile(repo_path):
            LOG.error(
                'Unable to sync {}. The path {} is a regular file'.format(
                    repo_name,
                    org_path,
                )
            )
            continue

        if not os.access(repo_path, os.W_OK | os.X_OK):
            LOG.error(
                'Unable to sync {}. The path {} is not writeable'.format(
                    repo_name,
                    org_path,
                )
            )
            continue

        if not os.path.exists(os.path.join(repo_path, '.git')):
            clone(repo_name, org, repo_path)
        else:
            fetch(repo_name, org, repo_path)


def sync(org, repos, target):
    do_sync(org, repos, target)
