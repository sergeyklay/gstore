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


from git import Repo
from .repo import RepoProgressPrinter
from .args import argparse
from .http import get_orgs, get_repos


def do_sync(org, repos, target):
    print('[INFO] sync repos for "{}"'.format(org))

    full_path = os.path.join(target, org)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    print('[INFO] total repos for "{}": {}'.format(org, len(repos)))
    for repo in repos:
        repo_path = os.path.join(full_path, repo)
        if not os.path.exists(os.path.join(repo_path, '.git')):
            if os.path.exists(repo_path):
                os.removedirs(repo_path)

            print('[NEW] ', repo, "doesn't exist. Clone ...")
            git_url = 'git@github.com:{}/{}.git'.format(org, repo)
            Repo.clone_from(git_url, repo_path, progress=RepoProgressPrinter())
        else:
            print('[SYNC]', repo, 'already exist. Sync ...')


def main():
    ns = argparse()
    orgs = ns.org

    if ns.org is None:
        orgs = get_orgs(ns.user, ns.token)

    for org in orgs:
        repos = get_repos(org, ns.token)
        do_sync(org, repos, ns.target)


if __name__ == '__main__':
    main()
