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

"""
A simple wrapper for github.GitHub to provide convenient way to clone and
sync repositories from the GitHub.
"""

import logging

from github import Github
from github.GithubException import BadCredentialsException
from github.GithubException import UnknownObjectException

from gstore import __version__
from gstore.exceptions import InvalidCredentialsError
from gstore.models import Organization, Repository

USER_AGENT = f'Gstore/{__version__}'

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
    :raise InvalidCredentialsError: in case of GitHub token is not provided.
    """

    def __init__(
            self,
            token: str,
            api_host=DEFAULT_HOST,
            timeout=DEFAULT_TIMEOUT,
    ):
        self.logger = logging.getLogger('gstore.client')

        if not token:
            raise InvalidCredentialsError(
                'GitHub token is not provided or it is empty')

        api_url = 'https://{}'.format(api_host)
        self.logger.debug('Setting API URL to %s', api_url)

        self.github = Github(
            login_or_token=token,
            base_url=api_url,
            timeout=timeout,
            user_agent=USER_AGENT
        )

    def get_repos(self, org: Organization):
        """
        Getting organization repositories.

        :param Organization org: User's organization
        :return: A collection with repositories
        :rtype: list of :class:`gstore.models.Repository`
        """
        self.logger.info('Getting repositories for organization')

        github_org = self.github.get_organization(org.login)
        repos = github_org.get_repos(
            type='all',
            sort='full_name'
        )

        self.logger.info(
            'Number of available repositories for %s organization: %s',
            org.login,
            repos.totalCount
        )

        retval = []
        for repo in repos:
            retval.append(Repository(repo.name, org))

        return retval

    def resolve_repos(self, repos: list, org: Organization):
        """
        Resolve repositories from provided list.

        :param list repos: A list of repositories in form 'org:repo'
        :param Organization org: User's organization
        :return: A collection with repositories
        :rtype: list of :class:`gstore.models.Repository`
        """
        self.logger.info('Resolve repositories from provided configuration')

        retval = []

        for name in repos:
            parts = name.split(':')

            if len(parts) != 2 or parts[0] == '' or parts[1] == '':
                self.logger.error(
                    'Invalid repo pattern: "%s", skip resolving',
                    name
                )
                continue

            if parts[0].lower() != org.login.lower():
                continue

            repo_name = parts[-1]

            try:
                # This will do API request, so we'll validate the repo.
                github_org = self.github.get_organization(org.login)
                repo = github_org.get_repo(repo_name)

                retval.append(Repository(repo.name, org))
            except UnknownObjectException:
                self.logger.error('Invalid repository name "%s"', repo_name)
                continue
            except BadCredentialsException as bad_credentials:
                raise InvalidCredentialsError(
                    'Bad token was used when accessing the GitHub API'
                ) from bad_credentials

        return retval

    def get_orgs(self):
        """
        Getting organizations for a user.

        :returns: A collection with organizations
        :rtype: list of :class:`gstore.models.Organization`
        """
        self.logger.info('Getting organizations for user')

        user = self.github.get_user()
        orgs = user.get_orgs()

        self.logger.info(
            'Number of available organizations for %s user: %s',
            user.login,
            orgs.totalCount
        )

        retval = []
        for org in orgs:
            retval.append(Organization(org.login))

        return retval

    def resolve_orgs(self, orgs: list):
        """
        Resolve organizations from provided list.

        :param list orgs: A list of organizations names
        :raise InvalidCredentialsError: in case of bad credentials.
        :return: A collection with organizations
        :rtype: list of :class:`gstore.models.Organization`
        """
        self.logger.info(
            'Resolve organizations from provided configuration')

        retval = []

        for name in orgs:
            try:
                # This will do API request, so we'll validate the org.
                org = self.github.get_organization(name)
                retval.append(Organization(org.login))
            except UnknownObjectException:
                self.logger.error('Invalid organization name "%s"', name)
                continue
            except BadCredentialsException as bad_credentials:
                raise InvalidCredentialsError(
                    'Bad token was used when accessing the GitHub API'
                ) from bad_credentials

        return retval
