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

from git import GitCommandError, Repo, RemoteProgress


class RepoProgressPrinter(RemoteProgress):
    """
    Extended progress printer
    """

    def update(self, op_code, cur_count, max_count=None, message=''):
        print(op_code, cur_count, max_count, cur_count /
              (max_count or 100.0), message or "NO MESSAGE")


def clone(repo_name, org, target):
    if os.path.exists(target):
        os.removedirs(target)

    print('[NEW] ', repo_name, "doesn't exist. Clone ...")
    git_url = 'git@github.com:{}/{}.git'.format(org, repo_name)

    try:
        Repo.clone_from(git_url, target, progress=RepoProgressPrinter())
    except GitCommandError as e:
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)


def fetch(repo_name, target):
    print('[SYNC]', repo_name, 'already exist. Sync ...')

    repo = Repo(target)

    try:
        repo.git.fetch(['--prune', '--quiet'])
        repo.git.pull(['--all', '--quiet'])
    except GitCommandError as e:
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)


def do_sync(org, repos, target):
    print('[INFO] sync repos for "{}"'.format(org))

    org_path = os.path.join(target, org)

    # Just in case create directories recursively
    if not os.path.exists(org_path):
        os.makedirs(org_path)

    print('[INFO] total repos for "{}": {}'.format(org, len(repos)))
    for repo_name in repos:
        repo_path = os.path.join(org_path, repo_name)

        if not os.path.exists(os.path.join(repo_path, '.git')):
            clone(repo_name, org, repo_path)
        else:
            fetch(repo_name, repo_path)


def sync(org, repos, target):
    do_sync(org, repos, target)
