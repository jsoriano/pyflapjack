#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


__version__ = '0.2.0'
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


install_requires = [
    'requests==2.5.1',
    'micromodels==0.5.1',
]
tests_require = install_requires + [
    'pytest==2.6.4', 'coverage==3.7.1', 'mock==1.0.1']
develop_require = tests_require + [
    'Sphinx>=1.2.1', 'pylint>=1.1.0']


setup(
    name='pyflapjack',
    version=__version__,
    description='Flapjack Python API',
    long_description=readme + '\n\n' + history,
    author='Detalytics',
    author_email='developer@detalytics.com',
    url='https://github.com/tryagainconepts/pyflapjack',
    packages=find_packages(),
    package_dir={'pyflapjack': 'pyflapjack'},
    install_requires=install_requires,
    extras_require={
        'develop': develop_require,
        'test': tests_require,
    },
    zip_safe=False,
    keywords='pyflapjack',
)
