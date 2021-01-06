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

"""The main entry point. Invoke as `gstore' or `python -m gstore'."""

import sys

from gstore.cli import main


def init():
    """
    Main entrypoint.

    This simple wrapper function runs the main() function when the file is
    executed by interpreter. Conversely, if the file is used as a module, the
    main() function will not automatically execute.

    The sys.exit() function is called with a return value of main(), as all
    good UNIX programs do.
    """
    if __name__ == '__main__':
        sys.exit(main())


init()
