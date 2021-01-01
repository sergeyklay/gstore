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

TOP := $(dir $(lastword $(MAKEFILE_LIST)))

# Run “make package” by default
.DEFAULT_GOAL = package

PYTHON    ?= python
PYTEST     = pytest
PYTEST_COV = pytest-cov
TWINE      = twine
FLAKE8     = flake8

# Program availability
HAVE_PYTHON := $(shell sh -c "command -v $(PYTHON)")
ifndef HAVE_PYTHON
$(warning "$(PYTHON) is not available.")
endif

HAVE_TWINE := $(shell sh -c "command -v $(TWINE)")
ifndef HAVE_TWINE
$(warning "$(TWINE) is not available.")
endif

HAVE_FLAKE8 := $(shell sh -c "command -v $(FLAKE8)")
ifndef HAVE_FLAKE8
$(warning "$(FLAKE8) is not available.")
endif

HAVE_PYTEST := $(shell sh -c "command -v $(PYTEST)")
ifndef HAVE_PYTEST
$(warning "$(PYTEST) is not available.")
endif

HAVE_PYTEST_COV =
ifdef HAVE_PYTHON
ifdef HAVE_PYTEST
HAVE_PYTEST_COV = $(shell sh -c "$(PYTHON) -m pip show $(PYTEST_COV) 2>/dev/null")
endif
endif

PACKAGE = $(shell sed -nre "s/PKG_NAME[[:space:]]*=[[:space:]]*'(.*)'/\1/p" $(TOP)/setup.py)
VERSION = $(shell sed -nre "s/^__version__[[:space:]]*=[[:space:]]*['\"](.*)['\"]/\1/p" $(TOP)/$(PACKAGE)/__init__.py)

ARCHIVE_NAME = $(PACKAGE)-$(VERSION)
WHL_NAME = $(PACKAGE)-$(VERSION)-py3-none-any

ARCHIVE_CONTENTS = CHANGELOG.rst \
	LICENSE \
	MANIFEST.in \
	README.rst \
	$(PACKAGE)/__init__.py \
	$(PACKAGE)/__main__.py \
	$(PACKAGE)/args.py \
	$(PACKAGE)/cli.py \
	$(PACKAGE)/client.py \
	$(PACKAGE)/exceptions.py \
	$(PACKAGE)/logger.py \
	$(PACKAGE)/repo.py \
	setup.cfg \
	setup.py
