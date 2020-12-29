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

import logging
import os

import git
from github.Organization import Organization
from github.Repository import Repository

from .exceptions import get_error


class RepoProgressPrinter(git.RemoteProgress):
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
        logging.getLogger('gstore.repo').debug('{} {} {} {} {}'.format(
            op_code,
            cur_count,
            max_count,
            cur_count / (max_count or 100.0),
            message or '',
        ))


class RepoManager:
    def __init__(self, base_path: str):
        self.base_path = os.path.expanduser(base_path).rstrip('/\\')
        self.logger = logging.getLogger('gstore.repo_manager')

    def clone(self, org: Organization, repo: Repository, target: str):
        self.logger.info('Clone repository to %s/%s', org.login, repo.name)

        if os.path.exists(target):
            os.removedirs(target)

        # TODO(serghei): Provide a way to configure git protocol
        git_url = 'git@github.com:%s/%s.git' % (org.login, repo.name)

        try:
            git.Repo.clone_from(
                git_url,
                target,
                progress=RepoProgressPrinter()
            )
        except git.GitCommandError as e:
            self.logger.error('Failed to clone %s/%s', org.login, repo.name)
            for msg in get_error(e):
                self.logger.error(msg)

    def fetch(self, org: Organization, repo: Repository, target: str):
        self.logger.info('Update repository in %s/%s', org.login, repo.name)

        local_repo = git.Repo(target)

        try:
            local_repo.git.fetch(['--prune', '--quiet'])
            local_repo.git.pull(['--all', '--quiet'])
        except git.GitCommandError as e:
            self.logger.error('Failed to update %s/%s', org.login, repo.name)
            for msg in get_error(e):
                self.logger.error(msg)

    def sync(self, org: Organization, repos):
        self.logger.info('Sync repos for %s', org.login)

        org_path = os.path.join(self.base_path, org.login)

        # Just in case create directories recursively
        if not os.path.exists(org_path):
            os.makedirs(org_path)

        for repo in repos:
            repo_path = os.path.join(org_path, repo.name)

            if os.path.exists(repo_path):
                if os.path.isfile(repo_path):
                    self.logger.error(
                        'Unable to sync %s. The path %s is a regular file',
                        repo.name,
                        repo_path,
                    )
                    continue

                if not os.access(repo_path, os.W_OK | os.X_OK):
                    self.logger.error(
                        'Unable to sync %s. The path %s is not writeable',
                        repo.name,
                        repo_path,
                    )
                    continue

            if os.path.exists(os.path.join(repo_path, '.git')):
                self.fetch(org, repo, repo_path)
            else:
                os.removedirs(repo_path)  # remove garbage
                self.clone(org, repo, repo_path)
