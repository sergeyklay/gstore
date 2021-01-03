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

import logging

from github import Github

from gstore import __version__
from .models import Organization, Repository

USER_AGENT = 'Gstore/{}'.format(__version__)

DEFAULT_HOST = 'api.github.com'
DEFAULT_TIMEOUT = 15

TOKEN_NAMES = (
    'GH_TOKEN',
    'GITHUB_TOKEN',
    'GH_ENTERPRISE_TOKEN',
    'GITHUB_ENTERPRISE_TOKEN',
)


class Client:
    """
    This is a wrapper class around :class:`github.Github` to interact with
    GitHub API.

    :param str token: Authentication token for github.com API requests
    :param str api_host: Default base URL for github.com API requests
    :param int timeout: Timeout for HTTP requests
    """

    def __init__(
            self,
            token: str,
            api_host=DEFAULT_HOST,
            timeout=DEFAULT_TIMEOUT,
    ):
        if not token:
            raise ValueError(
                'GitHub token was not provided but it is mandatory')

        api_url = 'https://{}'.format(api_host)

        self.github = Github(
            login_or_token=token,
            base_url=api_url,
            timeout=timeout,
            user_agent=USER_AGENT
        )

        self.logger = logging.getLogger('gstore.client')

    def get_repos(self, org: Organization):
        """
        Getting organization repositories.

        :param Organization org: User's organization
        :return: A collection with repositories
        :rtype: list of :class:`gstore.models.Repository`
        """
        self.logger.info('Getting repositories for %s organization', org.login)

        github_org = self.github.get_organization(org.login)
        repos = github_org.get_repos(
            type='all',
            sort='full_name'
        )

        self.logger.info(
            'Total number of repositories for %s: %s',
            org.login,
            repos.totalCount
        )

        retval = []
        for repo in repos:
            retval.append(Repository(repo.name))

        return retval

    def resolve_repos(self, repos: list, org: Organization):
        """
        Initialize repositories from provided list.

        :param list repos: A list of repositories in form 'org:repo'
        :param Organization org: User's organization
        :return: A collection with repositories
        :rtype: list of :class:`gstore.models.Repository`
        """
        self.logger.info('Initialize repositories from provided configuration')

        retval = []

        for name in repos:
            parts = name.split(':')
            # TODO(serghei): Check for parts[0] index
            if parts[0].lower() != org.login.lower():
                continue

            # This will do API request, so we'll validate the repo.
            # TODO(serghei): Catch exceptions here and do not add repo
            org = self.github.get_organization(org.login)
            repo = org.get_repo(parts[-1])

            retval.append(Repository(repo.name))

        return retval

    def get_orgs(self):
        """
        Getting organizations for a user.

        :returns: A collection with organizations
        :rtype: list of :class:`gstore.models.Organization`
        """
        self.logger.info('Getting organizations for a user')

        user = self.github.get_user()
        orgs = user.get_orgs()

        self.logger.info(
            'Total number of organizations for %s: %s',
            user.login,
            orgs.totalCount
        )

        retval = []
        for org in orgs:
            retval.append(Organization(org.login))

        return retval

    def resolve_orgs(self, orgs: list):
        """
        Initialize organizations from provided list.

        :param list orgs: A list of organizations names
        :return: A collection with organizations
        :rtype: list of :class:`gstore.models.Organization`
        """
        self.logger.info(
            'Initialize organizations from provided configuration')

        retval = []

        for name in orgs:
            # This will do API request, so we'll validate the org.
            # TODO(serghei): Catch exceptions here
            org = self.github.get_organization(name)

            retval.append(Organization(org.login))

        return retval
