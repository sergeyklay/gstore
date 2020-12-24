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

TOP := $(dir $(lastword $(MAKEFILE_LIST)))

# Run “make package” by default
.DEFAULT_GOAL = package

TWINE  ?= twine
PYTHON ?= python

# Program availability
HAVE_TWINE := $(shell sh -c "command -v $(TWINE)")
ifndef HAVE_TWINE
$(warning "$(TWINE) is not available.")
endif

HAVE_PYTHON := $(shell sh -c "command -v $(PYTHON)")
ifndef HAVE_PYTHON
$(warning "$(PYTHON) is not available.")
endif

VERSION = $(file < VERSION)

PACKAGE = gstore
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
	$(PACKAGE)/http.py \
	$(PACKAGE)/repo.py \
	setup.cfg \
	setup.py
