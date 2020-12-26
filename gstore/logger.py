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

import sys
import logging


class DebugFilter(logging.Filter):
    """
    Extended standard logging Filter to filer only DEBUG messages.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Only messages with record level DEBUG can pass
        for messages with another level an extra handler is used.

        :param tuple record: logging message record
        :returns: True|False
        :rtype: bool
        """
        return record.levelno == logging.DEBUG


class InfoFilter(logging.Filter):
    """
    Extended standard logging Filter to filer only INFO messages.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Only messages with record level INFO can pass
        for messages with another level an extra handler is used.

        :param tuple record: logging message record
        :returns: True|False
        :rtype: bool
        """
        return record.levelno == logging.INFO


def setup_logger(verbose=False):
    """
    Setup and return the root logger object for the application.
    """

    root = logging.getLogger('gstore')
    root.setLevel(logging.DEBUG)

    f = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(f)

    if verbose:
        debug_handler = logging.StreamHandler(sys.stdout)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.addFilter(DebugFilter())
        debug_handler.setFormatter(formatter)
        root.addHandler(debug_handler)

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(InfoFilter())
    info_handler.setFormatter(formatter)
    root.addHandler(info_handler)

    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(formatter)
    root.addHandler(error_handler)

    return root
