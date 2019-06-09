#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from codecs import open
import subprocess


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = open('VERSION').read().replace('\n', '')
readme = open('README.rst').read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()
else:
    if os.path.exists(os.path.join(os.path.dirname(__file__), '.git')):
        cmd = 'git rev-parse --verify --short HEAD'.split(' ')
        git_hash = subprocess.check_output(cmd).decode().replace('\n', '')
        version = "%s+git.%s" % (version, git_hash)


setup(
    name='django-cruds-adminlte',
    version=version,
    description="""django-cruds-adminlte is simple drop-in django app that creates CRUD for faster prototyping.""",  # noqa
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
        'django>=2.2',
        'django-crispy-forms==1.7.2',
        'djangoajax==2.3.7',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
