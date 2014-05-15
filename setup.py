#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from setuptools import setup, find_packages
import os.path

here = os.path.abspath(os.path.dirname(__file__))
#README = open(os.path.join(here, 'README.rst')).read()
#HISTORY = open(os.path.join(here, 'HISTORY.rst')).read()
HISTORY = """Unreleased as of yet"""

VERSION = '0.1.dev1'


install_requires = ['Flask', 'SQLAlchemy', 'Flask-SQLAlchemy',
                    'alembic']

setup_requires = []


args = dict(name='guessitserver',
            version=VERSION,
            description='Guessit server',
            long_description='Guessit server',
            # Get strings from
            # http://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers=['Development Status :: 2 - Pre-Alpha',
                         'License :: Other/Proprietary License',
                         'Operating System :: OS Independent',
                         'Programming Language :: Python :: 2',
                         'Programming Language :: Python :: 2.7',
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
