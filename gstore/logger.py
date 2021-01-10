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

"""Logging initialization for the gstore command-line tool."""

import logging
import sys


class DebugFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Extended standard logging Filter to filer only DEBUG messages."""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Only messages with record level DEBUG can pass
        for messages with another level an extra handler is used.

        :param tuple record: logging message record
        :returns: True|False
        :rtype: bool
        """
        return record.levelno == logging.DEBUG


class InfoFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Extended standard logging Filter to filer only INFO messages."""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Only messages with record level INFO can pass
        for messages with another level an extra handler is used.

        :param tuple record: logging message record
        :returns: True|False
        :rtype: bool
        """
        return record.levelno == logging.INFO


def setup_logger(verbose=False, quiet=False) -> logging.Logger:
    """Setup and return the root logger object for the application.

    :param bool verbose: Enable debug logging
    :param bool quiet: Disable info logging
    :rtype: :class:`logging.Logger`
    """

    root = logging.getLogger('gstore')
    root.setLevel(logging.ERROR if quiet else logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    specs = (
        {'on': verbose, 'filter': DebugFilter()},
        {'on': not quiet, 'level': logging.INFO, 'filter': InfoFilter()},
        {'on': True, 'stream': sys.stderr, 'level': logging.ERROR},
    )

    for spec in specs:
        if spec['on']:
            handler = logging.StreamHandler(spec.get('stream', sys.stdout))
            handler.setLevel(spec.get('level', logging.DEBUG))
            handler.setFormatter(formatter)

            if spec.get('filter'):
                handler.addFilter(spec['filter'])

            root.addHandler(handler)

    return root
