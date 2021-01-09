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

import pytest

from gstore import env


@pytest.mark.parametrize(
    'provided,expected',
    [
        ([{'k': 'GH_TOKEN', 'v': 'secret1'}], 'secret1'),
        ([{'k': 'GITHUB_TOKEN', 'v': 'secret2'}], 'secret2'),
        ([{'k': 'GITHUB_TOKEN', 'v': 'secret3'},
          {'k': 'GH_TOKEN', 'v': 'secret4'}], 'secret4'),
        ([{'k': 'GH_TOKEN', 'v': 'secret5'},
          {'k': 'GITHUB_TOKEN', 'v': 'secret6'}], 'secret5'),
        ([{'k': 'GH_ENTERPRISE_TOKEN', 'v': 'secret7'}], 'secret7'),
        ([{'k': 'GITHUB_ENTERPRISE_TOKEN', 'v': 'secret8'}], 'secret8'),
        ([{'k': 'GITHUB_ENTERPRISE_TOKEN', 'v': 'secret9'},
          {'k': 'GH_ENTERPRISE_TOKEN', 'v': 'secret10'}], 'secret10'),
        ([{'k': 'GH_ENTERPRISE_TOKEN', 'v': 'secret11'},
          {'k': 'GITHUB_ENTERPRISE_TOKEN', 'v': 'secret12'}], 'secret11'),
        ([{'k': 'GH_TOKEN', 'v': ''}], None),
        ([{'k': 'GITHUB_TOKEN', 'v': ''}], None),
        ([{'k': 'GH_ENTERPRISE_TOKEN', 'v': ''}], None),
        ([{'k': 'GITHUB_ENTERPRISE_TOKEN', 'v': ''}], None),
        ([{'k': 'GH_TOKEN', 'v': ''},
          {'k': 'GITHUB_TOKEN', 'v': ''},
          {'k': 'GH_ENTERPRISE_TOKEN', 'v': ''},
          {'k': 'GITHUB_ENTERPRISE_TOKEN', 'v': ''}], None),
    ]
)
def test_get_token(provided, expected, monkeypatch):
    """
    Call gstore.env.token_lookup() will return a token from environment
    variables (if any is set), taking into account the priority of these
    variables.
    """
    for m in provided:
        monkeypatch.setenv(m['k'], m['v'])

    assert env.token_lookup() == expected
