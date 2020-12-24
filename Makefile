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

include default.mk

dist/$(WHL_NAME).whl: $(ARCHIVE_CONTENTS)
	$(PYTHON) setup.py bdist_wheel

dist/$(ARCHIVE_NAME).tar.gz: $(ARCHIVE_CONTENTS)
	$(PYTHON) setup.py sdist

.PHONY: .title
.title:
	@echo "gstore $(VERSION)"

## Public targets

.PHONY: clean
clean:
	$(info Remove all build artefacts and directories...)
	@$(RM) -rf *.egg-info/ dist/ build/

.PHONY: check
check: package
	$(TWINE) check dist/*
	$(info Done.)

.PHONY: lint
lint:
	@$(FLAKE8) . --count --show-source --statistics
	@$(FLAKE8) . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

.PHONY: upload
upload: package
	$(TWINE) upload --repository testpypi dist/*
	$(info Done.)

.PHONY: package
package: dist/$(ARCHIVE_NAME).tar.gz dist/$(WHL_NAME).whl

.PHONY: help
help: .title
	@echo ''
	@echo 'Available targets:'
	@echo '  help:       Show this help and exit'
	@echo '  package:    Build gstore package'
	@echo '  upload:     Upload gstore distribution to the repository'
	@echo '  clean:      Remove all build artefacts and directories'
	@echo '  check:      Check distribution files'
	@echo '  lint:       Lint code'
	@echo ''
	@echo 'Available programs:'
	@echo '  $(PYTHON): $(if $(HAVE_PYTHON),yes,no)'
	@echo '  $(TWINE): $(if $(HAVE_TWINE),yes,no)'
	@echo '  $(FLAKE8): $(if $(HAVE_FLAKE8),yes,no)'
	@echo ''
	@echo 'You need $(TWINE) to develop gstore.'
	@echo 'See https://twine.readthedocs.io/en/latest for more'
	@echo ''
