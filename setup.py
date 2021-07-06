# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in eurocast/__init__.py
from eurocast import __version__ as version

setup(
	name='eurocast',
	version=version,
	description='Development for Eurocast',
	author='nxweb',
	author_email='info@nxweb.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
