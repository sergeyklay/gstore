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

include default.mk

define mk-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		echo $(ROOT_DIR) >  $(VENV_ROOT)/.project; \
		if [ ! -d $(WORKON_HOME)/gstore -a ! -L $(WORKON_HOME)/gstore ]; \
		then \
			ln -s $(ROOT_DIR)/$(VENV_ROOT) $(WORKON_HOME)/gstore; \
			echo ; \
			echo Since you use virtualenvwrapper, we created a symlink; \
			echo "so you can also use "workon gstore" to activate the venv."; \
			echo ; \
		fi; \
	fi
endef

define rm-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		if [ -L "$(WORKON_HOME)/gstore" -a -f "$(WORKON_HOME)/gstore" ]; \
		then \
			$(RM) $(WORKON_HOME)/gstore; \
		fi; \
	fi
endef

## Public targets

$(VENV_ROOT):
	@echo $(CS)Creating a Python environment $(VENV_ROOT)$(CE)
	$(PYTHON) -m venv --prompt gstore $(VENV_ROOT)
	@echo
	@echo Done.
	@echo
	@echo To active it manually, run:
	@echo
	@echo "    source $(VENV_BIN)/activate"
	@echo
	@echo See https://docs.python.org/3/library/venv.html for more.
	@echo
	$(call mk-venv-link)

.PHONY: init
init: $(VENV_ROOT)
	@echo $(CS)Installing dev requirements$(CE)
	$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
	$(VENV_PIP) install --upgrade -r $(REQUIREMENTS)
	$(VENV_PIP) install --upgrade -r $(REQUIREMENTS_DEV)

.PHONY: install
install: init
	@echo $(CS)Installing Gstore$(CE)
	$(VENV_PIP) install --upgrade --editable .

.PHONY: uninstall
uninstall:
	@echo $(CS)Uninstalling gstore$(CE)
	- $(VENV_PIP) uninstall --yes gstore &2>/dev/null

	@echo Verifying...
	cd .. && ! $(VENV_PYTHON) -m gstore --version &2>/dev/null

	@echo Done.
	@echo

.PHONY: clean
clean:
	@echo $(CS)Remove build and tests artefacts and directories$(CE)

	$(RM) -r $(VENV_ROOT)
	$(call rm-venv-link)
	find ./ -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r ./build ./dist ./*.egg-info
	$(RM) -r ./.cache ./.pytest_cache
	$(RM) -r ./htmlcov
	$(RM) ./.coverage ./coverage.xml

.PHONY: check-dist
check-dist: $(VENV_ROOT)
	@echo $(CS)Check distribution files$(HEADER_EXTRA)$(CE)
	$(VENV_BIN)/twine check ./dist/*
	$(VENV_BIN)/check-wheel-contents ./dist/*.whl
	@echo

.PHONY: test-ccov
test-ccov: COV=--cov=./gstore --cov=./tests --cov-report=xml --cov-report=html
test-ccov: HEADER_EXTRA=' (with coverage)'
test-ccov: test

.PHONY: test-all
test-all: uninstall clean install test test-dist lint

.PHONY: test-dist
test-dist: test-sdist test-wheel
	@echo

.PHONY: sdist
sdist:
	@echo $(CS)Creating source distribution$(CE)
	$(VENV_PYTHON) setup.py sdist

.PHONY: test-sdist
test-sdist: $(VENV_ROOT) sdist
	@echo $(CS)Testing source distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.gz
	@echo
	$(VENV_BIN)/gstore --version
	@echo

.PHONY: wheel
wheel:
	@echo $(CS)Creating wheel distribution$(CE)
	$(VENV_PYTHON) setup.py bdist_wheel

.PHONY: test-wheel
test-wheel: $(VENV_ROOT) wheel
	@echo $(CS)Testing built distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.whl
	@echo
	$(VENV_BIN)/gstore --version
	@echo

.PHONY: test
test:
	@echo $(CS)Running tests$(HEADER_EXTRA)$(CE)
	$(VENV_BIN)/py.test $(PYTEST_FLAGS) $(COV) ./gstore ./tests
	@echo

.PHONY: lint
lint:
	@echo $(CS)Running linters$(CE)
	$(VENV_BIN)/flake8 $(FLAKE8_FLAGS) ./
	$(VENV_BIN)/pylint ./gstore

.PHONY: publish
publish: test-all upload

.PHONY: upload
upload:
	@echo $(CS)Upload built distribution$(CE)
	@$(VENV_PYTHON) setup.py --version | grep -q "dev" && echo '!!! Not publishing dev version !!!' && exit 1 || echo ok
	$(MAKE) build
	$(MAKE) check-dist
	$(VENV_BIN)/twine upload ./dist/*
	@echo

.PHONY: build
build: sdist wheel
	@echo

.PHONY: help
help:
	@echo gstore
	@echo
	@echo 'Run "make init" first to install and update all dev dependencies.'
	@echo 'See "default.mk" for variables you might want to set.'
	@echo
	@echo 'Available targets:'
	@echo
	@echo '  help:         Show this help and exit'
	@echo '  venv:         Creating a Python environment (has to be launched first)'
	@echo '  init:         Installing dev requirements'
	@echo '  install:      Install development version of gstore'
	@echo '  uninstall:    Uninstall local version of gstore'
	@echo '  build:        Build gstore distribution (sdist and wheel)'
	@echo '  sdist:        Create a source distribution'
	@echo '  wheel:        Create a wheel distribution'
	@echo '  publish:      Publish gstore distribution to the repository'
	@echo '  upload:       Upload gstore distribution to the repository (w/o tests)'
	@echo '  clean:        Remove build and tests artefacts and directories'
	@echo '  check-dist:   Check integrity of the distribution files and validate package'
	@echo '  test:         Run unit tests'
	@echo '  test-dist:    Testing package distribution and installation'
	@echo '  test-sdist:   Testing source distribution and installation'
	@echo '  test-wheel:   Testing built distribution and installation'
	@echo '  test-all:     Test everything'
	@echo '  test-ccov:    Run unit tests with coverage'
	@echo '  lint:         Lint the code'
	@echo
	@echo 'Virtualenv:'
	@echo
	@echo '  Python:       $(VENV_PYTHON)'
	@echo '  pip:          $(VENV_PIP)'
	@echo
	@echo 'Flags:'
	@echo
	@echo '  FLAKE8_FLAGS: $(FLAKE8_FLAGS)'
	@echo '  PYTEST_FLAGS: $(PYTEST_FLAGS)'
	@echo
	@echo 'Environment variables:'
	@echo
	@echo '  PYTHON:       $(PYTHON)'
	@echo '  WORKON_HOME:  ${WORKON_HOME}'
	@echo '  SHELL:        $(shell echo $$SHELL)'
	@echo '  TERM:         $(shell echo $$TERM)'
	@echo
