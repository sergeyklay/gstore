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

from github import Github
from gstore import __version__


MAX_PAGES = 5000
USER_AGENT = 'Gstore/{}'.format(__version__)

DEFAULT_BASE_URL = 'https://api.github.com'
DEFAULT_TIMEOUT = 15

LOG = logging.getLogger('gstore.client')


def assert_token_is_present(token):
    """
    Check GitHub Personal Access Token.

    :param str token: Authentication token for github.com API requests
    """
    if not token:
        LOG.error('GitHub token was not provided but it is mandatory')
        exit(1)


class Client:
    def __init__(
            self,
            token: str,
            api_url=DEFAULT_BASE_URL,
            timeout=DEFAULT_TIMEOUT,
    ):
        """
        :param str token: Authentication token for github.com API requests
        :param str api_url: Default base URL for github.com API requests
        :param int timeout: Timeout for HTTP requests
        :param str user_agent: Default user agent to make HTTP requests
        """

        assert_token_is_present(token)

        self.github = Github(
            login_or_token=token,
            base_url=api_url,
            timeout=timeout,
            user_agent=USER_AGENT
        )

    def get_repos(self, org):
        """
        Getting organization repositories.

        :param str org: User's organization
        :return: A collection with repositories
        :rtype: list
        """
        LOG.info('Getting repositories for %s organization' % org)

        repos = self.github.get_organization(org).get_repos(
            type='all',
            sort='full_name'
        )

        LOG.info('Total number of repositories for %s: %d' %
                 (org, repos.totalCount))

        retval = []
        for repo in repos:
            retval.append(repo.name)

        return retval

    def get_orgs(self):
        """
        Getting organizations for a user.

        :returns: A collection with organizations
        :rtype: list
        """
        LOG.info('Getting organizations for a user')

        user = self.github.get_user()
        orgs = user.get_orgs()

        LOG.info('Total number of organizations for %s: %d' %
                 (user.login, orgs.totalCount))

        retval = []
        for org in orgs:
            retval.append(org.login)

        return retval
