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

import json
import requests

API_URL = 'https://api.github.com'
MAX_PAGES = 5000


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
