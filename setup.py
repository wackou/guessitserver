#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessItServer - Providing http access points to GuessIt
# Copyright (c) 2014 Nicolas Wack <wackou@gmail.com>
#
# GuessItServer is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessItServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages
import os.path

here = os.path.abspath(os.path.dirname(__file__))
#README = open(os.path.join(here, 'README.rst')).read()
#HISTORY = open(os.path.join(here, 'HISTORY.rst')).read()
HISTORY = """Unreleased as of yet"""

VERSION = '0.1.dev1'


install_requires = ['Flask', 'SQLAlchemy', 'Flask-SQLAlchemy',
                    'alembic', 'guessit']

setup_requires = []


args = dict(name='guessitserver',
            version=VERSION,
            description='Guessit server',
            long_description='Guessit server',
            # Get strings from
            # http://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers=['Development Status :: 2 - Pre-Alpha',
                         'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                         'Operating System :: OS Independent',
                         'Programming Language :: Python :: 2',
                         'Programming Language :: Python :: 2.7',
                         'Programming Language :: Python :: 3',
                         'Programming Language :: Python :: 3.3',
                         'Programming Language :: Python :: 3.4'
                         ],
            keywords='guessit server',
            author='Nicolas Wack',
            author_email='wackou@gmail.com',
            url='http://bugs.guessit.io/',
            packages=find_packages(),
            include_package_data=True,
            #package_data = { 'guessitserver': ['guessitserver/static/css/*'] },
            install_requires=install_requires,
            setup_requires=setup_requires,
            )

setup(**args)
