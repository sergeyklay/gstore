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
        ([('GH_TOKEN', 'secret1')], 'secret1'),
        ([('GITHUB_TOKEN', 'secret2')], 'secret2'),
        ([('GITHUB_TOKEN', 'secret3'),
          ('GH_TOKEN', 'secret4')], 'secret4'),
        ([('GH_TOKEN', 'secret5'),
          ('GITHUB_TOKEN', 'secret6')], 'secret5'),
        ([('GH_ENTERPRISE_TOKEN', 'secret7')], 'secret7'),
        ([('GITHUB_ENTERPRISE_TOKEN', 'secret8')], 'secret8'),
        ([('GITHUB_ENTERPRISE_TOKEN', 'secret9'),
          ('GH_ENTERPRISE_TOKEN', 'secret10')], 'secret10'),
        ([('GH_ENTERPRISE_TOKEN', 'secret11'),
          ('GITHUB_ENTERPRISE_TOKEN', 'secret12')], 'secret11'),
        ([('GH_TOKEN', '')], None),
        ([('GITHUB_TOKEN', '')], None),
        ([('GH_ENTERPRISE_TOKEN', '')], None),
        ([('GITHUB_ENTERPRISE_TOKEN', '')], None),
        ([('GH_TOKEN', ''),
          ('GITHUB_TOKEN', ''),
          ('GH_ENTERPRISE_TOKEN', ''),
          ('GITHUB_ENTERPRISE_TOKEN', '')], None),
    ])
def test_lookup_token(provided, expected, monkeypatch):
    """Call gstore.env.lookup_token() will return a token from environment
    variables (if any is set), taking into account the priority of these
    variables.
    """
    for k, v in provided:
        monkeypatch.setenv(k, v)

    assert env.lookup_token() == expected


@pytest.mark.parametrize(
    'provided,expected',
    [
        (None, None),
        ('', None),
        ('secret', 'secret'),
    ]
)
def test_get_host(provided, expected, monkeypatch):
    """Call gstore.env.get_host() will return a host if environment
    variable is set with not empty string, otherwise None.
    """
    if provided is None:
        monkeypatch.delenv('GH_HOST', raising=False)
    else:
        monkeypatch.setenv('GH_HOST', provided)

    assert env.get_host() == expected


@pytest.mark.parametrize(
    'provided,expected',
    [
        (None, None),
        ('', None),
        ('~/backup', '~/backup'),
    ]
)
def test_get_target(provided, expected, monkeypatch):
    """Call gstore.env.get_target() will return a target if environment
    variable is set with not empty string, otherwise None.
    """
    if provided is None:
        monkeypatch.delenv('GSTORE_DIR', raising=False)
    else:
        monkeypatch.setenv('GSTORE_DIR', provided)

    assert env.get_target() == expected
