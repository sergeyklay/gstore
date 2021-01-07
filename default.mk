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

TOP      := $(dir $(lastword $(MAKEFILE_LIST)))
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifneq (,$(findstring xterm,${TERM}))
	GREEN := $(shell tput -Txterm setaf 2)
	RESET := $(shell tput -Txterm sgr0)
	CS = "${GREEN}~~~ "
	CE = " ~~~${RESET}"
else
	CS = "~~~ "
	CE = " ~~~"
endif

COV =
HEADER_EXTRA =

REQUIREMENTS = requirements.txt
REQUIREMENTS_DEV = requirements-dev.txt

PYTEST_FLAGS ?= --verbose --color=yes

# Run “make build” by default
.DEFAULT_GOAL = build

# Will used to create venv
ifeq ($(OS),Windows_NT)
	PYTHON ?= python
else
	PYTHON ?= python3
endif

VENV_ROOT=.venv

ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV_ROOT)/Scripts
else
	VENV_BIN=$(VENV_ROOT)/bin
endif

VENV_PIP=$(VENV_BIN)/pip
VENV_PYTHON=$(VENV_BIN)/python

export PATH := $(VENV_BIN):$(PATH)

# Program availability
HAVE_PYTHON := $(shell sh -c "command -v $(PYTHON)")
ifndef HAVE_PYTHON
$(error "$(PYTHON) is not available.")
endif

PACKAGE = $(shell sed -nEe "s/PKG_NAME[[:space:]]*=[[:space:]]*'(.*)'/\1/p" $(TOP)setup.py)
VERSION = $(shell sed -nEe "s/^__version__[[:space:]]*=[[:space:]]*['\"](.*)['\"]/\1/p" $(TOP)$(PACKAGE)/__init__.py)

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
	$(PACKAGE)/models.py \
	$(PACKAGE)/repo.py \
	setup.cfg \
	setup.py
