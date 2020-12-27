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

from .args import argparse
from .client import Client
from .logger import setup_logger
from .repo import sync


def main():
    ns = argparse()
    setup_logger(verbose=ns.verbose, quiet=ns.quiet)

    logger = logging.getLogger('gstore.cli')

    try:
        client = Client(token=ns.token, api_host=ns.host)

        if ns.org is None:
            orgs = client.get_orgs()
        else:
            orgs = ns.org

        for org in orgs:
            repos = client.get_repos(org)
            sync(org, repos, ns.target)
    except Exception as e:
        logger.critical(e)
