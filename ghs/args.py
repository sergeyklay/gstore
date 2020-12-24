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

from argparse import ArgumentParser


def argparse():
    parser = ArgumentParser(
        description="Synchronize organizations' repositories from GitHub.")

    parser.add_argument('--user', dest='user',
                        help='username to get organizarions list')
    parser.add_argument('--token', dest='token', required=True,
                        help='personal auth token')
    parser.add_argument('--org', dest='org', nargs='*',
                        help='organizations you have access to (deault "all")')
    parser.add_argument('target',
                        help='base target to sync repos (e.g. folder on disk)')

    return parser.parse_args()
