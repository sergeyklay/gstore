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

import codecs
import re
from os import path

from setuptools import setup, find_packages


def locate_package_directory():
    """Identify a directory of the package and its associated files."""
    try:
        return path.abspath(path.dirname(__file__))
    except Exception as path_error:
        message = ('The directory in which the package and its '
                   'associated files are stored could not be located.')
        raise RuntimeError(message) from path_error


def read_file(filepath):
    """Read content from a UTF-8 encoded text file."""
    with codecs.open(filepath, 'rb', 'utf-8') as file_handle:
        return file_handle.read()


PKG_NAME = 'gstore'
PKG_DIR = locate_package_directory()
META_PATH = path.join(PKG_DIR, PKG_NAME, '__init__.py')
META_CONTENTS = read_file(META_PATH)


def load_long_description():
    """Load long description from file README.rst."""
    def changes():
        changelog = path.join(PKG_DIR, 'CHANGELOG.rst')
        pat = r"(\d+.\d.\d \(.*?\)\r?\n.*?)\r?\n\r?\n\r?\n----\r?\n\r?\n\r?\n"
        result = re.search(pat, read_file(changelog), re.S)

        if result:
            return result.group(1)
        else:
            return ''

    try:
        read_me = path.join(PKG_DIR, 'README.rst')
        authors = path.join(PKG_DIR, 'AUTHORS.rst')

        title = f"{PKG_NAME}: {find_meta('description')}\n"
        head = '=' * len(title) + '\n'

        contents = (
            head
            + format(title.strip(' .'))
            + head
            + read_file(read_me).split('.. teaser-begin')[1]
            + "\n\n"
            + "Release Information\n"
            + "===================\n\n"
            + changes()
            + "\n\n`Full changelog "
            + f"<{find_meta('url')}/en/latest/changelog.html>`_.\n\n"
            + read_file(authors)
        )

        return contents
    except Exception as read_error:
        message = 'Long description could not be read from README.rst'
        raise RuntimeError(message) from read_error


def is_canonical_version(version):
    """Check if a version string is in the canonical format of PEP 440."""
    pattern = (
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))'
        r'*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))'
        r'?(\.dev(0|[1-9][0-9]*))?$')
    return re.match(pattern, version) is not None


def find_meta(meta):
    """Extract __*meta*__ from META_CONTENTS."""
    meta_match = re.search(
        r"^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]".format(meta=meta),
        META_CONTENTS,
        re.M
    )

    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(
        f'Unable to find __{meta}__ string in package meta file')


def get_version_string():
    """Return package version as listed in `__version__` in meta file."""
    # Parse version string
    version_string = find_meta('version')

    # Check validity
    if not is_canonical_version(version_string):
        message = (
            'The detected version string "{}" is not in canonical '
            'format as defined in PEP 440.'.format(version_string))
        raise ValueError(message)

    return version_string


KEYWORDS = [
    'git',
    'github',
    'backup',
    'repo',
    'sync',
]

# Classifiers: available ones listed at https://pypi.org/classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',

    'Environment :: Console',

    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Information Technology',

    'Natural Language :: English',

    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa: E501
    'Operating System :: OS Independent',

    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3 :: Only',

    'Topic :: System :: Archiving :: Backup',
    'Topic :: System :: Software Distribution',
    'Topic :: Software Development :: Build Tools',
    'Topic :: Software Development :: Version Control',
    'Topic :: Software Development :: Version Control :: Git',
]

# Dependencies that are downloaded by pip on installation and why.
INSTALL_REQUIRES = [
    'PyGithub>=1.54.1',  # Interact with GitHub objects
    'gitpython>=3.0.6',  # Interact with Git repositories
]

# List additional groups of dependencies here (e.g. testing dependencies).
# You can install these using the following syntax, for example:
#
#    $ pip install -e .[develop,testing]
#
EXTRAS_REQUIRE = {
    # Dependencies that are required to run tests
    'testing': [
        'pytest>=6.2.2',  # Our tests framework
        'pytest-cov>=2.11.1',  # Pytest plugin for measuring coverage
        'pylint>=2.6.0,!=2.6.1',  # Python code static checker
        'flake8>=3.8.4',  # The modular source code checker
    ],
    'develop': [
        'twine>=3.3.0',  # Publishing packages on PyPI
        'setuptools>=53.0.0',  # Build and install packages
        'wheel>=0.36.2',  # A built-package format for Python
        'check-wheel-contents>=0.2.0',  # Check wheels have the right contents
    ],
    'docs': [
        'furo>=2020.12.30b24,==2020.12.*',  # Sphinx documentation theme
        'sphinx>=3.5.0',  # Python documentation generator
    ],
}

# Project's URLs
PROJECT_URLS = {
    'Documentation': 'https://gstore.readthedocs.io',
    'Bug Tracker': 'https://github.com/sergeyklay/gstore/issues',
    'Source Code': 'https://github.com/sergeyklay/gstore',
}

ENTRY_POINTS = {
    'console_scripts': [
        f'{PKG_NAME}={PKG_NAME}.cli:main'
    ]
}

if __name__ == '__main__':
    setup(
        name=PKG_NAME,
        version=get_version_string(),
        author=find_meta('author'),
        author_email=find_meta('author_email'),
        maintainer=find_meta('author'),
        maintainer_email=find_meta('author_email'),
        license=find_meta('license'),
        description=find_meta('description'),
        long_description=load_long_description(),
        long_description_content_type='text/x-rst',
        keywords=KEYWORDS,
        url=find_meta('url'),
        project_urls=PROJECT_URLS,
        classifiers=CLASSIFIERS,
        packages=find_packages(),
        platforms='any',
        include_package_data=True,
        zip_safe=False,
        python_requires='>=3.7, <4',
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        entry_points=ENTRY_POINTS,
    )
