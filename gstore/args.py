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
import sys
import textwrap as _textwrap
from argparse import ArgumentParser, HelpFormatter
from os import environ as env

from gstore import __copyright__, __version__
from .client import DEFAULT_HOST, TOKEN_NAMES


class LineBreaksFormatter(HelpFormatter):
    """ArgParse help formatter that allows line breaks in the usage messages
    and argument help strings.

    Normally to include newlines in the help output of argparse, you have
    use argparse.RawDescriptionHelpFormatter. However, this means raw text is
    enabled everywhere, and not just for specific help entries where we may
    need it.

    This help formatter allows for you to optional enable/toggle raw text on
    individual menu items by prefixing the help string with 'n|'."""

    def _fill_text(self, text, width, indent):
        text = self._whitespace_matcher.sub(' ', text).strip()
        paragraphs = text.split('|n ')

        multiline_text = ''

        for paragraph in paragraphs:
            formatted_paragraph = _textwrap.fill(
                paragraph,
                width,
                initial_indent=indent,
                subsequent_indent=indent
            ) + '\n'

            multiline_text = multiline_text + formatted_paragraph

        return multiline_text


def get_version_str():
    version = '''
    {prog}s {version}|n
    {copy}.|n
    This is free software; see the source for copying conditions.  There is NO|n
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    '''.format(  # noqa E501
        prog='%(prog)',
        version=__version__,
        copy=__copyright__,
    )
    return version


def get_token_from_env():
    """
    Get authentication token for GitHub API from environment variables.

    The order of searching for a token in environment variables:
    * GH_TOKEN, GITHUB_TOKEN (in order of precedence)
    * GH_ENTERPRISE_TOKEN, GITHUB_ENTERPRISE_TOKEN (in order of precedence)

    :returns: An authentication token for github.com API requests
    :rtype: str|None
    """
    token = None

    for name in TOKEN_NAMES:
        token = env.get(name)
        if token:
            break

    return token


def argparse():
    p = ArgumentParser(
        description='Synchronize GitHub repositories of your organizations.',
        formatter_class=LineBreaksFormatter)

    dumpversion_help = ("print the version of the program and don't " +
                        'do anything else')

    quiet_help = 'silence any informational messages, but not error ones'
    token = get_token_from_env()

    p.add_argument('target', nargs='?', type=str,
                   default=env.get('GSTORE_DIR', os.getcwd()),
                   help='base target to sync repos (e.g. folder on disk)')

    p.add_argument('--token', dest='token', default=token, type=str,
                   help='an authentication token for GitHub API requests')
    p.add_argument('--host', dest='host',
                   default=env.get('GH_HOST', DEFAULT_HOST), type=str,
                   help='the GitHub API hostname (by default api.github.com)')
    p.add_argument('--org', dest='org', nargs='*', type=str,
                   help='organizations you have access to (by default all)')
    p.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                   help='enable verbose mode')
    p.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                   help=quiet_help)
    p.add_argument('-V', '--version', action='version',
                   help="print program's version information and quit",
                   version=get_version_str())
    p.add_argument('-dumpversion', action='version', help=dumpversion_help,
                   version=__version__)

    if len(sys.argv) == 1 and token is None:
        p.print_help(sys.stderr)
        sys.exit(1)

    return p.parse_args()
