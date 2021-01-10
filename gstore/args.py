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

"""Command line argument parsing methods for gstore."""

import os
import sys
import textwrap as _textwrap
from argparse import SUPPRESS, ArgumentParser, HelpFormatter, Namespace

from gstore import __copyright__, __version__
from gstore import env


class LineBreaksFormatter(HelpFormatter):
    """
    ArgParse help formatter that allows line breaks in the usage messages
    and argument help strings.

    Normally to include newlines in the help output of argparse, you have
    use argparse.RawDescriptionHelpFormatter. However, this means raw text is
    enabled everywhere, and not just for specific help entries where we may
    need it.

    This help formatter allows for you to optional enable/toggle raw text on
    individual menu items by prefixing the help string with 'n|'."""
    def _fill_text(self, text, width, indent) -> str:
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


def get_version_str() -> str:
    """A helper function to format version info."""
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


def parser_add_positionals(parser: ArgumentParser) -> ArgumentParser:
    """Add positional parameters group to a parser."""
    pgroup = parser.add_argument_group('Positional parameters')

    pgroup.add_argument('target', nargs='?', type=str,
                        default=env.get_target() or os.getcwd(),
                        help='Base target to sync repos (e.g. folder on disk)')

    return parser


def parser_add_options(parser: ArgumentParser) -> ArgumentParser:
    """Add options group to a parser."""
    token = env.lookup_token()

    ogroup = parser.add_argument_group('Options')

    ogroup.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Print this help message and quit')

    ogroup.add_argument('--token', dest='token', default=token, type=str,
                        help='An authentication token for GitHub API requests')

    ogroup.add_argument('--host', dest='host', default=env.lookup_token(),
                        type=str, help='The GitHub API hostname')

    ogroup.add_argument('-o', '--org', dest='org', action='append', type=str,
                        help='Organization to sync (all if not provided)')

    repo_help = ('Limit sync to the specified repository, ' +
                 'otherwise sync all repositories (format "org:repo")')
    ogroup.add_argument('-r', '--repo', dest='repo', action='append',
                        type=str, help=repo_help)

    ogroup.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Increase output verbosity')

    quiet_help = 'Silence any informational messages, but not error ones'
    ogroup.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                        help=quiet_help)

    ogroup.add_argument('-V', '--version', action='version',
                        help="Print program's version information and quit",
                        version=get_version_str())

    dumpversion_help = ("Print the version of the program and don't " +
                        'do anything else')
    ogroup.add_argument('-dumpversion', action='version',
                        help=dumpversion_help, version=__version__)

    return parser


def argparse() -> Namespace or None:
    """
    The function initializes command line arguments parser.

    This function will show help message and return None if gstore was called
    without any argument and environment variables were not enough to start
    gstore.

    :return: The list of parsed arguments or None in case of any error.
    :rtype: :class:`argparse.Namespace` or None
    """
    parser = ArgumentParser(
        description='Synchronize GitHub repositories of your organizations.',
        usage='%(prog)s [options] [[--] target]',
        formatter_class=LineBreaksFormatter,
        add_help=False,
    )

    parser_add_positionals(parser)
    parser_add_options(parser)

    if len(sys.argv) == 1 and env.lookup_token() is None:
        parser.print_help(sys.stderr)
        return None

    return parser.parse_args()
