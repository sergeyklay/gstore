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
	$(PYTHON) setup.py bdist_wheel

dist/$(ARCHIVE_NAME).tar.gz: $(ARCHIVE_CONTENTS)
	$(PYTHON) setup.py sdist

.PHONY: .title
.title:
	@echo "$(PACKAGE) $(VERSION)"

## Public targets

.PHONY: install
install:
	@echo $(H1)Installing dev requirements$(H1END)
	$(PYTHON) -m pip install --upgrade -r $(REQUIREMENTS)

	@echo $(H1)Installing Gstore$(H1END)
	$(PYTHON) -m pip install --upgrade --editable .

.PHONY: uninstall
uninstall:
	@echo $(H1)Uninstalling $(PACKAGE)$(H1END)
	- $(PYTHON) -m pip uninstall --yes $(PACKAGE) &2>/dev/null

	@echo "Verifying..."
	cd .. && ! $(PYTHON) -m $(PACKAGE) --version &2>/dev/null

	@echo "Done"
	@echo

.PHONY: clean
clean:
	@echo $(H1)Remove build and tests artefacts and directories$(H1END)

	find $(TOP) -name '__pycache__' -delete -o -name '*.pyc' -delete
	$(RM) -r $(TOP)build $(TOP)dist $(TOP)*.egg-info
	$(RM) -r $(TOP).tox $(TOP).pytest_cache
	$(RM) -r $(TOP)htmlcov
	$(RM) $(TOP).coverage $(TOP)coverage.xml

.PHONY: check-dist
check-dist:
	@echo $(H1)Check distribution files$(HEADER_EXTRA)$(H1END)
	$(TWINE) check $(TOP)dist/*
	@echo

.PHONY: test-ccov
test-ccov: COV=--cov
test-ccov: HEADER_EXTRA=' (with coverage)'
test-ccov: test

.PHONY: test-all
test-all: clean install lint test test-dist

.PHONY: test-dist
test-dist: test-sdist test-bdist
	@echo

.PHONY: test-sdist
test-sdist: clean dist/$(ARCHIVE_NAME).tar.gz
	@echo $(H1)Testing source distribution and installation$(H1END)
	$(PYTHON) -m pip install --force-reinstall --upgrade dist/*.gz
	@echo
	$(PACKAGE) --version
	@echo

.PHONY: test-bdist
test-bdist: clean dist/$(WHL_NAME).whl
	@echo $(H1)Testing built distribution and installation$(H1END)
	$(PYTHON) -m pip install --force-reinstall --upgrade dist/*.whl
	@echo
	$(PACKAGE) --version
	@echo

.PHONY: test
test:
	@echo $(H1)Running tests$(HEADER_EXTRA)$(H1END)
	$(PYTEST) $(COV) $(TOP)$(PACKAGE) $(COV) $(TOP)tests --verbose $(TOP)$(PACKAGE) $(TOP)tests
	@echo

.PHONY: lint
lint:
	$(FLAKE8) $(TOP) --count --show-source --statistics
	$(FLAKE8) $(TOP) --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

.PHONY: publish
publish: test-all upload

.PHONY: upload
upload:
	@echo $(H1)Upload built distribution$(H1END)
	@echo "$(VERSION)"
	@echo "$(VERSION)" | grep -q "dav" && echo '!!! Not publishing dev version !!!' && exit 1 || echo ok
	$(MAKE) build
	$(MAKE) check-dst
	$(TWINE) upload $(TOP)dist/*
	@echo

.PHONY: build
build: dist/$(ARCHIVE_NAME).tar.gz dist/$(WHL_NAME).whl
	@echo

.PHONY: help
help: .title
	@echo ''
	@echo 'Available targets:'
	@echo '  help:       Show this help and exit'
	@echo '  install:    Install development version of $(PACKAGE)'
	@echo '  uninstall:  Uninstall $(PACKAGE)'
	@echo '  build:      Build $(PACKAGE) distribution'
	@echo '  publish:    Publish $(PACKAGE) package'
	@echo '  upload:     Upload $(PACKAGE) distribution to the repository'
	@echo '                (meant for "publish")'
	@echo '  clean:      Remove build and tests artefacts and directories'
	@echo '  check-dist: Check integrity of distribution files'
	@echo '                and validate packages'
	@echo '  test:       Run unit tests'
	@echo '  test-dist:  Testing package distribution and installation'
	@echo '  test-sdist: Testing source distribution and installation'
	@echo '  test-bdist: Testing built distribution and installation'
	@echo '  test-all:   Test everything'
	@echo '  test-ccov:  Run unit tests with coverage'
	@echo '  lint:       Lint the code'
	@echo ''
	@echo 'Available programs:'
	@echo '  python:     $(if $(HAVE_PYTHON),yes,no)'
	@echo '  twine:      $(if $(HAVE_TWINE),yes,no)'
	@echo '  flake8:     $(if $(HAVE_FLAKE8),yes,no)'
	@echo '  pytest:     $(if $(HAVE_PYTEST),yes,no)'
	@echo '  pytest-cov: $(if $(HAVE_PYTEST_COV),yes,no)'
	@echo ''
	@echo 'You need $(TWINE) to develop $(PACKAGE).'
	@echo 'See https://twine.readthedocs.io/en/latest for more'
	@echo ''
