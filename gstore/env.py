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

"""Helper routines to work with environment variables.

Provides a convenient way to work with environment variables
used by various functions within Gstore.

Functions:

    lookup_token() -> str or None
    get_host() -> str or None
    get_target() -> str or None

Data:

    TOKEN_NAMES

"""

import os

TOKEN_NAMES = (
    'GH_TOKEN',
    'GITHUB_TOKEN',
    'GH_ENTERPRISE_TOKEN',
    'GITHUB_ENTERPRISE_TOKEN',
)


def lookup_token() -> str or None:
    """Lookup a personal access token from environment variables.

    This function looks for token variable in the following order:

        1. GH_TOKEN
        2. GITHUB_TOKEN
        3. GH_ENTERPRISE_TOKEN
        4. GITHUB_ENTERPRISE_TOKEN

    :returns: A personal access token if any or None
    :rtype: str or None
    """
    for name in TOKEN_NAMES:
        token = os.environ.get(name)
        if token:
            return token

    return None


def get_host() -> str or None:
    """Get GitHub API hostname from GH_HOST environment variable.

    This function may return None if there is no environment
    variable, or it is empty.

    :returns: The GitHub API hostname if any or None
    :rtype: str or None
    """
    return os.environ.get('GH_HOST') or None


def get_target() -> str or None:
    """Get base target to sync repos.

    This function may return None if there is no environment
    variable, or it is empty.

    :returns: The GitHub API hostname if any or None
    :rtype: str or None
    """
    return os.environ.get('GSTORE_DIR') or None
