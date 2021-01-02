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

from .args import argparse
from .client import Client
from .logger import setup_logger
from .repo import RepoManager


def main():
    args = argparse()
    setup_logger(verbose=args.verbose, quiet=args.quiet)

    logger = logging.getLogger('gstore.cli')

    try:
        client = Client(token=args.token, api_host=args.host)

        if args.org is None:
            orgs = client.get_orgs()
        else:
            orgs = client.resolve_orgs(args.org)

        manager = RepoManager(args.target)

        for org in orgs:
            repos = client.get_repos(org)
            manager.sync(org, repos)
    except Exception as ex:
        logger.critical(ex)
