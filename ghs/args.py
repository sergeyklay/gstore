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

from argparse import ArgumentParser


def argparse():
    p = ArgumentParser(
        description="Synchronize organizations' repositories from GitHub.")

    p.add_argument('--user', dest='user',
                   help='username to use to get organizations list')
    p.add_argument('--token', dest='token', required=True,
                   help='personal auth token')
    p.add_argument('--org', dest='org', nargs='*',
                   help='organizations you have access to (by default all)')
    p.add_argument('target', nargs='?',
                   default=os.environ.get('GHS_DIR', os.getcwd()),
                   help='base target to sync repos (e.g. folder on disk)')

    return p.parse_args()
