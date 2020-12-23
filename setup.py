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

from setuptools import setup, find_packages

setup(
    name='ghsync',
    version='0.0.1',
    author='Serghei Iakovlev',
    author_email='egrep@protonmail.ch',
    url='https://github.com/sergeyklay/ghsync',
    license='GPLv3+',
    packages=find_packages(),
    description="A simple cli tool to synchronize organizations'"
                'repositories from GitHub.',
    long_description=open('README.rst').read() + '\n\n',
    long_description_content_type='text/x-rst',
    keywords='git, github, backup, repo, sync',
    platforms='any',
    python_requires='>=3.6, <4',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Natural Language :: English',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: System :: Archiving :: Backup',
        'Topic :: Software Development :: Version Control :: Git',
    ],
    entry_points={
        'console_scripts': [
            'ghsync=ghsync.cli:main'
        ]
    },
    project_urls={
        'Bug Reports': 'https://github.com/sergeyklay/ghsync/issues',
        'Source': 'https://github.com/sergeyklay/ghsync',
    },
)
