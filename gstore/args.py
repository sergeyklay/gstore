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

from os import environ as env
from argparse import ArgumentParser


def get_token_from_env():
    """
    Get authentication token for github.com from environment variables.

    The order of searching for a token in environment variables:
    * GH_TOKEN, GITHUB_TOKEN (in order of precedence)
    * GH_ENTERPRISE_TOKEN, GITHUB_ENTERPRISE_TOKEN (in order of precedence)

    :returns: An authentication token for github.com API requests
    :rtype: str|None
    """
    token = None
    toke_names = (
        'GH_TOKEN',
        'GITHUB_TOKEN',
        'GH_ENTERPRISE_TOKEN',
        'GITHUB_ENTERPRISE_TOKEN',
    )

    for name in toke_names:
        token = env.get(name)
        if token:
            break

    return token


def argparse():
    p = ArgumentParser(
        description="Synchronize organizations' repositories from GitHub.")

    p.add_argument('target', nargs='?',
                   default=env.get('GSTORE_DIR', os.getcwd()),
                   help='base target to sync repos (e.g. folder on disk)')

    p.add_argument('--token', dest='token', default=get_token_from_env(),
                   help='an authentication token for github.com API requests')
    p.add_argument('--org', dest='org', nargs='*',
                   help='organizations you have access to (by default all)')
    p.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                   help='enable verbose mode')

    return p.parse_args()
