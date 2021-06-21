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
PKG_NAME = gstore

ifneq (,$(findstring xterm,${TERM}))
	GREEN := $(shell tput -Txterm setaf 2)
	RESET := $(shell tput -Txterm sgr0)
	CS = "${GREEN}~~~ "
	CE = " ~~~${RESET}"
else
	CS = "~~~ "
	CE = " ~~~"
endif

# Check for pyenv-virtualenv
ifndef PYENV_VIRTUALENV_INIT
VENV_ROOT = .venv
else
VENV_ROOT = $(shell sh -c "echo $$(pyenv root)/versions/$(PKG_NAME)")
endif

# PYTHON will used to create venv
ifeq ($(OS),Windows_NT)
	PYTHON  ?= python
	VENV_BIN = $(VENV_ROOT)/Scripts
else
	PYTHON  ?= python3
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
$(error "Python is not available please install Python")
endif
endif
endif
