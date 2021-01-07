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

dist/$(WHL_NAME).whl: $(ARCHIVE_CONTENTS)
	$(VENV_PYTHON) setup.py bdist_wheel

dist/$(ARCHIVE_NAME).tar.gz: $(ARCHIVE_CONTENTS)
	$(VENV_PYTHON) setup.py sdist

.PHONY: .title
.title:
	@echo $(PACKAGE) $(VERSION)

define mk-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		echo $(ROOT_DIR) >  $(VENV_ROOT)/.project; \
		if [ ! -d $(WORKON_HOME)/$(PACKAGE) -a ! -L $(WORKON_HOME)/$(PACKAGE) ]; \
		then \
			ln -s $(ROOT_DIR)/$(VENV_ROOT) $(WORKON_HOME)/$(PACKAGE); \
			echo ; \
			echo Since you use virtualenvwrapper, we created a symlink; \
			echo "so you can also use "workon $(PACKAGE)" to activate the venv."; \
			echo ; \
		fi; \
	fi
endef

define rm-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		if [ -L "$(WORKON_HOME)/$(PACKAGE)" -a -f "$(WORKON_HOME)/$(PACKAGE)" ]; \
		then \
			$(RM) $(WORKON_HOME)/$(PACKAGE); \
		fi; \
	fi
endef

## Public targets

$(VENV_ROOT):
	@echo $(CS)Creating a Python environment $(VENV_ROOT)$(CE)
	$(PYTHON) -m venv --prompt $(PACKAGE) $(VENV_ROOT)
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

# $(VENV_PIP) install --upgrade pip setuptools wheel
.PHONY: install
install: $(VENV_ROOT)
	@echo $(CS)Installing dev requirements$(CE)
	$(VENV_PIP) install --upgrade -r $(REQUIREMENTS)
	$(VENV_PIP) install --upgrade -r $(REQUIREMENTS_DEV)

	@echo $(CS)Installing Gstore$(CE)
	$(VENV_PIP) install --upgrade --editable .

.PHONY: uninstall
uninstall:
	@echo $(CS)Uninstalling $(PACKAGE)$(CE)
	- $(VENV_PIP) uninstall --yes $(PACKAGE) &2>/dev/null

	@echo Verifying...
	cd .. && ! $(VENV_PYTHON) -m $(PACKAGE) --version &2>/dev/null

	@echo Done.
	@echo

.PHONY: clean
clean:
	@echo $(CS)Remove build and tests artefacts and directories$(CE)

	$(RM) -r $(VENV_ROOT)
	$(call rm-venv-link)
	find $(TOP) -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r $(TOP)build $(TOP)dist $(TOP)*.egg-info
	$(RM) -r $(TOP).cache $(TOP).pytest_cache
	$(RM) -r $(TOP)htmlcov
	$(RM) $(TOP).coverage $(TOP)coverage.xml

.PHONY: check-dist
check-dist: $(VENV_ROOT)
	@echo $(CS)Check distribution files$(HEADER_EXTRA)$(CE)
	$(VENV_BIN)/twine check $(TOP)dist/*
	@echo

.PHONY: test-ccov
test-ccov: COV=--cov=$(TOP)$(PACKAGE) --cov=$(TOP)tests --cov-report=xml --cov-report=html
test-ccov: HEADER_EXTRA=' (with coverage)'
test-ccov: test

.PHONY: test-all
test-all: clean install test test-dist lint

.PHONY: test-dist
test-dist: test-sdist test-bdist
	@echo

.PHONY: test-sdist
test-sdist: clean $(VENV_ROOT) dist/$(ARCHIVE_NAME).tar.gz
	@echo $(CS)Testing source distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.gz
	@echo
	$(VENV_BIN)/$(PACKAGE) --version
	@echo

.PHONY: test-bdist
test-bdist: clean $(VENV_ROOT) dist/$(WHL_NAME).whl
	@echo $(CS)Testing built distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.whl
	@echo
	$(VENV_BIN)/$(PACKAGE) --version
	@echo

.PHONY: test
test:
	@echo $(CS)Running tests$(HEADER_EXTRA)$(CE)
	$(VENV_BIN)/py.test $(PYTEST_FLAGS) $(COV) $(TOP)$(PACKAGE) $(TOP)tests
	@echo

.PHONY: lint
lint:
	@echo $(CS)Running linters$(CE)
	$(VENV_BIN)/flake8 $(TOP) --count --show-source --statistics
	$(VENV_BIN)/flake8 $(TOP) --count --max-complexity=10 --statistics
	$(VENV_BIN)/pylint $(TOP)$(PACKAGE)

.PHONY: publish
publish: test-all upload

.PHONY: upload
upload:
	@echo $(CS)Upload built distribution$(CE)
	@echo "$(VERSION)"
	@echo "$(VERSION)" | grep -q "dav" && echo '!!! Not publishing dev version !!!' && exit 1 || echo ok
	$(MAKE) build
	$(MAKE) check-dst
	$(VENV_BIN)/twine upload $(TOP)dist/*
	@echo

.PHONY: build
build: dist/$(ARCHIVE_NAME).tar.gz dist/$(WHL_NAME).whl
	@echo

.PHONY: help
help: .title
	@echo
	@echo 'Run "make venv" first to install and update all dev dependencies.'
	@echo 'See "default.mk" for variables you might want to set.'
	@echo
	@echo 'Available targets:'
	@echo '  help:       Show this help and exit'
	@echo '  venv:       Creating a Python environment (has to be launched first)'
	@echo '  install:    Install development version of $(PACKAGE)'
	@echo '  uninstall:  Uninstall $(PACKAGE)'
	@echo '  build:      Build $(PACKAGE) distribution'
	@echo '  publish:    Publish $(PACKAGE) distribution to the repository'
	@echo '  upload:     Upload $(PACKAGE) distribution to the repository (w/o tests)'
	@echo '  clean:      Remove build and tests artefacts and directories'
	@echo '  check-dist: Check integrity of distribution files and validate packages'
	@echo '  test:       Run unit tests'
	@echo '  test-dist:  Testing package distribution and installation'
	@echo '  test-sdist: Testing source distribution and installation'
	@echo '  test-bdist: Testing built distribution and installation'
	@echo '  test-all:   Test everything'
	@echo '  test-ccov:  Run unit tests with coverage'
	@echo '  lint:       Lint the code'
	@echo
	@echo 'Used variables:'
	@echo '  PYTHON=$(PYTHON)'
	@echo '  VENV_PYTHON=$(VENV_PYTHON)'
	@echo '  VENV_PIP=$(VENV_PIP)'
	@echo '  SHELL=$(shell echo $$SHELL)'
	@echo '  TERM=$(shell echo $$TERM)'
	@echo '  TOP=$(TOP)'
	@echo '  ROOT_DIR=$(ROOT_DIR)'
	@echo
