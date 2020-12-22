import os
import json
import requests

from git import Repo
from argparse import ArgumentParser


API_URL = 'https://api.github.com'


def argparse():
    parser = ArgumentParser(
        description='Locally sync all GitHub repos & branches for user/org.')

    parser.add_argument('--token', dest='token', required=True,
                        help='personal auth token')
    parser.add_argument('--org', dest='org', required=True,
                        help='organization for access to')
    parser.add_argument('workdir', help='Base path to sync repos')

    return parser.parse_args()


def repos(org, token):
    endpoint = '/orgs/{}/repos'.format(org)
    url = '{}{}'.format(API_URL, endpoint)
    params = {'per_page': 100, 'type': 'all', 'sort': 'full_name'}
    headers = {'Accept': 'application/vnd.github.v3+json',
               'Authorization': 'token {}'.format(token)}

    retval = []
    for i in range(1, 5000 + 1):
        params['page'] = i
        response = requests.get(url=url, params=params, headers=headers)
        parsed_response = json.loads(response.text)

        if len(parsed_response) == 0:
            break

        for i in parsed_response:
            retval.append(i['name'])

    return retval


def sync(org, repos, workdir):
    full_path = os.path.join(workdir, org)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    print('total repos:', len(repos))
    for repo in repos:
        repo_path = os.path.join(full_path, repo)
        if not os.path.exists(os.path.join(repo_path, '.git')):
            if os.path.exists(repo_path):
                os.removedirs(repo_path)

            print('[NEW] ', repo, "doesn't exist. Clone ...")
            git_url = 'git@github.com:{}/{}.git'.format(org, repo)
            Repo.clone_from(git_url, repo_path)
        else:
            print('[SYNC]', repo, 'already exist. Sync ...')

    # print(workdir)
    # print(repos)


def main():
    ns = argparse()
    print('arguments:', ns)

    all_repos = repos(ns.org, ns.token)
    sync(ns.org, all_repos, ns.workdir)


if __name__ == '__main__':
    main()
