#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.0.11'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()

setup(
    name='django-cruds-adminlte',
    version=version,
    description="""django-cruds-adminlte is simple drop-in django app that creates CRUD for faster prototyping.""",  # noqa
    test_suite="runtests.run_tests",
    long_description=readme,
    author='Óscar M. Lage',
    author_email='info@oscarmlage.com',
    url='https://github.com/oscarmlage/django-cruds-adminlte',
    packages=[
        'cruds_adminlte',
        'cruds_adminlte.templatetags',

    ],
    include_package_data=True,
    install_requires=[
        'django-crispy-forms',
        'djangoajax',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-cruds-adminlte',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
