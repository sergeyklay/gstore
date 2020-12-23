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
import json
import requests

from git import Repo, RemoteProgress
from argparse import ArgumentParser


API_URL = 'https://api.github.com'
MAX_PAGES = 5000


class RepoProgressPrinter(RemoteProgress):
    """
    Extended progress printer
    """

    def update(self, op_code, cur_count, max_count=None, message=''):
        print(op_code, cur_count, max_count, cur_count /
              (max_count or 100.0), message or "NO MESSAGE")


def argparse():
    parser = ArgumentParser(
        description="Synchronize organizations' repositories from GitHub.")

    parser.add_argument('--user', dest='user',
                        help='username to get organizarions list')
    parser.add_argument('--token', dest='token', required=True,
                        help='personal auth token')
    parser.add_argument('--org', dest='org', nargs='*',
                        help='organizations you have access to (deault "all")')
    parser.add_argument('target',
                        help='base target to sync repos (e.g. folder on disk)')

    return parser.parse_args()


def create_headers(token):
    return {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token {}'.format(token)
    }


def collect_data(url, params, headers, key):
    retval = []

    for i in range(MAX_PAGES):
        params['page'] = i + 1
        response = requests.get(url=url, params=params, headers=headers)
        parsed_response = json.loads(response.text)

        if len(parsed_response) == 0:
            break

        for data in parsed_response:
            retval.append(data[key])

    return retval


def get_repos(org, token):
    print('[INFO] getting repositories list')

    endpoint = '/orgs/{}/repos'.format(org)
    url = '{}{}'.format(API_URL, endpoint)
    params = {'per_page': 100, 'type': 'all', 'sort': 'full_name'}
    headers = create_headers(token)

    return collect_data(url=url, params=params, headers=headers, key='name')


def get_orgs(user, token):
    print('[INFO] getting organizations list')

    if user is None:
        print('[ERR]  username is required to get organizations list')
        exit(1)

    endpoint = '/users/{}/orgs'.format(user)
    url = '{}{}'.format(API_URL, endpoint)
    params = {'per_page': 100}
    headers = create_headers(token)

    return collect_data(url=url, params=params, headers=headers, key='login')


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
