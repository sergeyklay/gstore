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

# Run “make build” by default
.DEFAULT_GOAL = build

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

COV          =
HEADER_EXTRA =

REQUIREMENTS     = requirements.txt
REQUIREMENTS_DEV = requirements-dev.txt

PYTEST_FLAGS ?= --color=yes -v
FLAKE8_FLAGS ?= --show-source --statistics

VENV_ROOT = .venv

# PYTHON will used to create venv
ifeq ($(OS),Windows_NT)
PYTHON  ?= python
VENV_BIN = $(VENV_ROOT)/Scripts
NULL     = NUL
else
PYTHON  ?= python3
VENV_BIN = $(VENV_ROOT)/bin
NULL     = /dev/null
endif

VENV_PIP    = $(VENV_BIN)/pip
VENV_PYTHON = $(VENV_BIN)/python

export PATH := $(VENV_BIN):$(PATH)

# Program availability
ifndef PYTHON
$(error "Python is not available please install Python")
else
PYTHON_VERSION := $(shell $(PYTHON) --version 2>$(NULL))
ifndef PYTHON_VERSION
$(error "Python is not available please install Python")
endif
endif
