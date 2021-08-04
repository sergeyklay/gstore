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
	@if [ -n "$(WORKON_HOME)" ] ; then \
		echo $(ROOT_DIR) > $(VENV_ROOT)/.project; \
		if [ ! -d $(WORKON_HOME)/$(PKG_NAME) -a ! -L $(WORKON_HOME)/$(PKG_NAME) ]; \
		then \
			ln -s $(ROOT_DIR)/$(VENV_ROOT) $(WORKON_HOME)/$(PKG_NAME); \
			echo ; \
			echo Since you use virtualenvwrapper, we created a symlink; \
			echo "so you can also use "workon $(PKG_NAME)" to activate the venv."; \
			echo ; \
		fi; \
	fi
endef

define rm-venv-link
	@if [ -n "$(WORKON_HOME)" ]; then \
		if [ -L "$(WORKON_HOME)/$(PKG_NAME)" -a -f "$(WORKON_HOME)/$(PKG_NAME)" ]; \
		then \
			$(RM) $(WORKON_HOME)/$(PKG_NAME); \
		fi; \
	fi
endef

# '--generate-hashes' is disabled until we support Python 3.7
# and depend on 'typing_extensions'
requirements.txt: requirements.in $(VENV_BIN)
	$(VENV_BIN)/pip-compile --output-file=$@ $<

## Public targets

$(VENV_PYTHON): $(VENV_ROOT)
	@echo

$(VENV_ROOT):
	@echo $(CS)Creating a Python environment $(VENV_ROOT)$(CE)
	$(PYTHON) -m venv --prompt $(PKG_NAME) $(VENV_ROOT)
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
init: $(VENV_PYTHON)
	@echo $(CS)Set up virtualenv$(CE)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install --upgrade --use-feature=in-tree-build pip-tools wheel setuptools

.PHONY: install
install: requirements.txt
	@echo $(CS)Installing $(PKG_NAME) and all its dependencies$(CE)
	$(VENV_BIN)/pip-sync requirements.txt
	$(VENV_PIP) install --upgrade --editable .[develop]

.PHONY: uninstall
uninstall:
	@echo $(CS)Uninstalling $(PKG_NAME)$(CE)
	- $(VENV_PIP) uninstall --yes $(PKG_NAME) &2>/dev/null

	@echo Verifying...
	cd .. && ! $(VENV_PYTHON) -m $(PKG_NAME) --version &2>/dev/null

	@echo Done.
	@echo

.PHONY: clean
clean:
	@echo $(CS)Remove build and tests artefacts and directories$(CE)
	find ./ -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r ./build ./dist ./*.egg-info
	$(RM) -r ./.tox/reports
	@echo

.PHONY: maintainer-clean
maintainer-clean: clean
	@echo $(CS)Performing full clean$(CE)
	$(RM) -r $(VENV_ROOT)
	$(call rm-venv-link)
	$(RM) -r ./.tox
	$(RM) requirements.txt
	@echo

.PHONY: lint
lint: $(VENV_PYTHON)
	@echo $(CS)Running linters$(CE)
	tox -e lint

.PHONY: test
test: $(VENV_PYTHON)
	@echo $(CS)Running tests$(CE)
	tox -e py39

.PHONY: ccov
ccov:
	@echo $(CS)Combine coverage reports$(CE)
	tox -e coverage-report

.PHONY: manifest
manifest:
	@echo $(CS)Check MANIFEST.in for completeness$(CE)
	tox -e manifest

.PHONY: docs
docs:
	@echo $(CS)Build package documentation$(CE)
	tox -e docs

.PHONY: build
build: manifest sdist wheel
	@echo

.PHONY: check-dist
check-dist: $(VENV_PYTHON)
	@echo $(CS)Check distribution files$(CE)
	$(VENV_PIP) install twine check-wheel-contents
	$(VENV_BIN)/twine check ./dist/*
	$(VENV_BIN)/check-wheel-contents ./dist/*.whl

.PHONY: test-all
test-all: uninstall clean install test test-dist lint
	@echo

.PHONY: test-dist
test-dist: test-sdist test-wheel

.PHONY: sdist
sdist:
	@echo $(CS)Creating source distribution$(CE)
	$(VENV_PYTHON) setup.py sdist

.PHONY: test-sdist
test-sdist: $(VENV_PYTHON) sdist
	@echo $(CS)Testing source distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.gz
	@echo
	$(VENV_BIN)/$(PKG_NAME) --version

.PHONY: wheel
wheel: $(VENV_PYTHON)
	@echo $(CS)Creating wheel distribution$(CE)
	$(VENV_PYTHON) setup.py bdist_wheel

.PHONY: test-wheel
test-wheel: $(VENV_PYTHON) wheel
	@echo $(CS)Testing built distribution and installation$(CE)
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.whl
	@echo
	$(VENV_BIN)/$(PKG_NAME) --version

.PHONY: publish
publish: test-all upload

.PHONY: upload
upload: $(VENV_PYTHON)
	@echo $(CS)Upload built distribution$(CE)
	@$(VENV_PYTHON) setup.py --version | grep -q "dev" && echo '!!! Not publishing dev version !!!' && exit 1 || echo ok
	$(MAKE) build
	$(MAKE) check-dist
	$(VENV_BIN)/twine upload ./dist/*

.PHONY: help
help:
	@echo $(PKG_NAME)
	@echo
	@echo 'Run "make init" first to install and update all dev dependencies.'
	@echo 'See "default.mk" for variables you might want to set.'
	@echo
	@echo 'Available targets:'
	@echo
	@echo '  help:         Show this help and exit'
	@echo '  init:         Set up virtualenv (has to be launched first)'
	@echo '  install:      Install project and all its dependencies'
	@echo '  uninstall:    Uninstall local version of the project'
	@echo '  build:        Build $(PKG_NAME) distribution (sdist and wheel)'
	@echo '  sdist:        Creating source distribution'
	@echo '  wheel:        Creating wheel distribution'
	@echo '  publish:      Publish $(PKG_NAME) distribution to the repository'
	@echo '  upload:       Upload $(PKG_NAME) distribution to the repository (w/o tests)'
	@echo '  check-dist:   Check integrity of the distribution files and validate package'
	@echo '  manifest:     Check MANIFEST.in in a source package'
	@echo '  docs:         Build package documentation (HTML)'
	@echo '  lint:         Lint the code'
	@echo '  test:         Run unit tests with coverage'
	@echo '  test-dist:    Testing package distribution and installation'
	@echo '  test-sdist:   Testing source distribution and installation'
	@echo '  test-wheel:   Testing built distribution and installation'
	@echo '  test-all:     Test everything'
	@echo '  ccov:         Combine coverage reports'
	@echo '  clean:        Remove build and tests artefacts and directories'
	@echo '  maintainer-clean:'
	@echo '                Delete almost everything that can be reconstructed'
	@echo '                with this Makefile'
	@echo
	@echo 'Virtualenv:'
	@echo
	@echo '  Python:       $(VENV_PYTHON)'
	@echo '  pip:          $(VENV_PIP)'
	@echo
	@echo 'Environment variables:'
	@echo
	@echo '  PYTHON:       $(PYTHON)'
	@echo '  WORKON_HOME:  ${WORKON_HOME}'
	@echo '  SHELL:        $(shell echo $$SHELL)'
	@echo '  TERM:         $(shell echo $$TERM)'
	@echo
