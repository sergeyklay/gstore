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

from .args import argparse
from .client import get_orgs, get_repos, ensure_token_is_present
from .repo import sync
from .logger import setup_logger


def main():
    ns = argparse()

    setup_logger()
    ensure_token_is_present(ns.token)

    if ns.org is None:
        orgs = get_orgs(ns.token)
    else:
        orgs = ns.org

    for org in orgs:
        repos = get_repos(org, ns.token)
        sync(org, repos, ns.target)
