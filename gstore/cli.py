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

"""The CLI entry point. Invoke as `gstore' or `python -m gstore'."""

import logging
import signal
import sys

from gstore.args import argparse
from gstore.client import Client
from gstore.exceptions import Error
from gstore.logger import setup_logger
from gstore.repo import RepoManager


def main():
    """The main function to call gstore from the command line.

    :return: An exit code
    :rtype: int
    """
    args = argparse()
    retval = int(args is None)

    if args:
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
                if args.repo is None:
                    repos = client.get_repos(org)
                else:
                    repos = client.resolve_repos(args.repo, org)

                manager.sync(org, repos)
        except KeyboardInterrupt:  # the user hit control-C
            sys.stderr.write('Received keyboard interrupt, terminating.\n')
            sys.stderr.flush()
            # Control-C is fatal error signal 2, for more see
            # https://tldp.org/LDP/abs/html/exitcodes.html
            retval = 128 + signal.SIGINT
        except Error as gstore_error:
            logger.error(gstore_error)
            retval = 1

    return retval
