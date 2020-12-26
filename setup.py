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

import re
import sys

from os import path
from setuptools import setup, find_packages


def check_python_version():
    """
    Check Python's version.
    """

    if sys.version_info >= (4, 0):
        sys.stderr.write(
            'ERROR: This module is not supported with Python >= 4.0\n')
        sys.exit(1)

    if sys.version_info < (3, 6):
        sys.stderr.write('ERROR: This module requires at least Python 3.6\n')
        sys.exit(1)


def locate_package_directory():
    """
    Identify a directory of the package and its associated files.
    """

    try:
        return path.abspath(path.dirname(__file__))
    except Exception:
        message = ('The directory in which the package and its '
                   'associated files are stored could not be located.')
        raise ValueError(message)


def read_file(filepath):
    """
    Read content from a UTF-8 encoded text file.
    """

    with open(filepath, 'r', encoding='utf-8') as file_handle:
        text = file_handle.read()
    return text


def load_long_description(pkg_dir):
    """
    Load long description from file README.rst.
    """

    try:
        filepath_readme = path.join(pkg_dir, 'README.rst')
        return read_file(filepath_readme)
    except Exception:
        message = 'Long description could not be read from README.rst'
        raise ValueError(message)


# Source: https://www.python.org/dev/peps/pep-0440
def is_canonical_version(version):
    """
    Check if a version string is in the canonical format of PEP 440.
    """

    pattern = (
        r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))'
        r'*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))'
        r'?(\.dev(0|[1-9][0-9]*))?$')
    return re.match(pattern, version) is not None


def get_version_string(pkg_dir, pkg_name):
    """
    Read __version__ string for an init file.
    """

    try:
        # Read init file contents
        init_file = path.join(pkg_dir, pkg_name, '__init__.py')
        init_contents = read_file(init_file)

        # Parse version string
        re_version = re.compile(r'''__version__\s+=\s+['"](.*)['"]''')
        match = re_version.search(init_contents)
        if not match:
            message = ("Version couldn't be parsed from variable "
                       '__version__ in file __init__.py')
            raise ValueError(message)
        version_string = match.group(1)
    except Exception:
        message = ("Version couldn't be read from variable "
                   '__version__ in file __init__.py')
        raise ValueError(message)

    # Check validity
    if not is_canonical_version(version_string):
        message = (
            'The detected version string "{}" is not in canonical '
            'format as defined in PEP 440.'.format(version_string))
        raise ValueError(message)

    return version_string


PKG_NAME = 'gstore'
PKG_DIR = locate_package_directory()


check_python_version()

setup(
    # Basic package information
    name=PKG_NAME,
    version=get_version_string(PKG_DIR, PKG_NAME),
    author='Serghei Iakovlev',
    author_email='egrep@protonmail.ch',
    maintainer='Serghei Iakovlev',
    maintainer_email='egrep@protonmail.ch',
    url='https://github.com/sergeyklay/gstore',
    license='GPLv3+',
    description='Gstore is a simple tool to synchronize GitHub '
                'repositories of your organizations.',
    long_description=load_long_description(PKG_DIR),
    long_description_content_type='text/x-rst',
    keywords='git github backup repo sync',
    project_urls={
        'Tracker': 'https://github.com/sergeyklay/gstore/issues',
        'Source': 'https://github.com/sergeyklay/gstore',
    },

    # Classifiers: available ones listed at https://pypi.org/classifiers
    classifiers=[
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Software Distribution',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Version Control :: Git',
    ],

    # Included files
    # a) auto-detected Python packages
    packages=find_packages(),
    # b) data files that are specified in the MANIFEST.in file
    include_package_data=True,

    # Dependencies that need to be fulfilled
    platforms='any',
    python_requires='>=3.6, <4',

    # Dependencies that are downloaded by pip on installation and why
    install_requires=[
        'PyGithub>=1.54.1',  # Interact with GitHub objects
        'gitpython>=3.0.6',  # Interact with Git repositories
    ],

    # Entry points
    entry_points={
        'console_scripts': [
            '{pkg}={pkg}.cli:main'.format(pkg=PKG_NAME)
        ]
    },

    # Capability of running in compressed form: yes
    zip_safe=True,
)
