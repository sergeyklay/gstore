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


.PHONY: clean
clean:
	@echo $(H1)Remove Python cache ...$(H1END)
	find $(TOP) -name '__pycache__' -delete -o -name '*.pyc' -delete
	@echo $(H1)Remove all build artefacts and directories...$(H1END)
	$(RM) -r $(TOP)build $(TOP)dist $(TOP)*.egg-info
	@echo $(H1)Remove tests artefacts ...$(H1END)
	$(RM) -r $(TOP).tox $(TOP).pytest_cache
	@echo $(H1)Remove code coverage artefacts ...$(H1END)
	$(RM) -r $(TOP)htmlcov
	$(RM) $(TOP).coverage $(TOP)coverage.xml

.PHONY: check
check: build
	$(TWINE) check $(TOP)dist/*
	$(info Done.)

.PHONY: test-ccov
test-ccov: COV=--cov
test-ccov: HEADER_EXTRA=' (with coverage)'
test-ccov: test

.PHONY: test
test:
	@echo $(H1)Running tests$(HEADER_EXTRA)$(H1END)
	$(PYTEST) $(COV) $(TOP)$(PACKAGE) $(COV) $(TOP)tests --verbose $(TOP)$(PACKAGE) $(TOP)tests
	@echo

.PHONY: lint
lint:
	$(FLAKE8) $(TOP) --count --show-source --statistics
	$(FLAKE8) $(TOP) --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

.PHONY: upload
publish: build
	$(TWINE) upload $(TOP)dist/*
	$(info Done.)

.PHONY: build
build: dist/$(ARCHIVE_NAME).tar.gz dist/$(WHL_NAME).whl

.PHONY: help
help: .title
	@echo ''
	@echo 'Available targets:'
	@echo '  help:       Show this help and exit'
	@echo '  install:    Install development version of $(PACKAGE)'
	@echo '  build:      Build $(PACKAGE) distribution'
	@echo '  publish:    Upload $(PACKAGE) distribution to the repository'
	@echo '  clean:      Remove all build artefacts and directories'
	@echo '  check:      Check distribution files'
	@echo '  test:       Run unit tests'
	@echo '  test-ccov:  Run unit tests with coverage'
	@echo '  lint:       Lint code'
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
