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

from unittest import mock


def test_init():
    """This rather bulky test assures that our init function does everything
    it should:

        - Really calls main if we have '__name__' equals to '__main__'
        - Returns it return value as exit code
        - Does not call main() otherwise

    The final line of the code, the init() call will run at the module import
    time and, therefore, is run at test time.
    """
    from gstore import __main__ as module
    with mock.patch.object(module, 'main', return_value=42):
        with mock.patch.object(module, '__name__', '__main__'):
            with mock.patch.object(module.sys, 'exit') as mock_exit:
                module.init()
                assert mock_exit.call_args[0][0] == 42
