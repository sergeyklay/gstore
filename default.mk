# Copyright (C) 2020, 2021, 2022, 2023 Serghei Iakovlev <egrep@protonmail.ch>
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

# Run “make build” by default
.DEFAULT_GOAL = build

ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PKG_NAME = gstore

PYLINT_FLAGS ?=
FLAKE8_FLAGS ?=

ifneq ($(TERM),)
	GREEN := $(shell tput setaf 2)
	RESET := $(shell tput sgr0)
	CS = "${GREEN}~~~ "
	CE = " ~~~${RESET}"

	PYTEST_FLAGS ?= --color=yes
else
	CS = "~~~ "
	CE = " ~~~"

	PYTEST_FLAGS ?=
endif

COV          =
REQUIREMENTS = requirements/requirements.txt requirements/requirements-dev.txt

ifneq ($(VIRTUAL_ENV),)
	VENV_ROOT = $(VIRTUAL_ENV)
else
	VENV_ROOT = .venv
endif

# PYTHON will used to create venv
ifeq ($(OS),Windows_NT)
	PYTHON  ?= python.exe
	VIRTUALENV ?= virtualenv.exe
	VENV_BIN = $(VENV_ROOT)/Scripts
else
	PYTHON  ?= python3
	VIRTUALENV ?= $(PYTHON) -m venv
	VENV_BIN = $(VENV_ROOT)/bin
endif

VENV_PYTHON = $(VENV_BIN)/python
VENV_PIP    = $(VENV_PYTHON) -m pip

export PATH := $(VENV_BIN):$(PATH)

# Program availability
ifndef PYTHON
$(error "Python is not available please install Python")
else
ifneq ($(OS),Windows_NT)
HAVE_PYTHON := $(shell sh -c "command -v $(PYTHON)")
ifndef HAVE_PYTHON
$(error "Python is not available. Please install Python.")
endif
endif
endif
