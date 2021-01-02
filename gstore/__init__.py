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

"""Gstore is a simple tool to synchronize GitHub repositories of your
organizations.

This tool uses the GitHub API to get a list of all forked, mirrored, public,
and private repos owned by your organizations. If the repo already exists
locally, it will update it via git-pull. Otherwise, it will properly clone the
repo.

Please refer to the documentation provided in the README.rst, which can be
found at Gstore's PyPI URL: https://pypi.org/project/gstore/
"""

__copyright__ = 'Copyright (C) 2020, 2021 Serghei Iakovlev'
__version__ = '0.2.1'
__license__ = 'GPLv3+'
__author__ = 'Serghei Iakovlev'
__author_email__ = 'egrep@protonmail.ch'
__url__ = 'https://github.com/sergeyklay/gstore'
