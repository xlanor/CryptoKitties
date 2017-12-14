#! /usr/bin/env python3
#-*- coding: utf-8 -*-
##
# Cryptokitty setup.py
#
##
import os, sys,contextlib,pip

try:
	from setuptools import setup, find_packages
except ImportError:
	from distutils.core import setup, find_packages


name = "CryptoKitties TG Bot"

rootdir = os.path.abspath(os.path.dirname(__file__))

links=[]
requires=[]

#Python 3.4 and above
if sys.version_info < (3, 4, 0, 'final', 0):
	raise SystemExit ('Python 3.4 or later is required!')

#Opening requirements.txt to obtain a list of libraries needed

	# new versions of pip requires a session
requirements = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

for item in requirements:
	# we want to handle package names and also repo urls
	if getattr(item, 'url', None):  # older pip has url
		links.append(str(item.url))
	if getattr(item, 'link', None): # newer pip has link
		links.append(str(item.link))
	if item.req:
		requires.append(str(item.req))

setup(
		name='CryptoKitties TG Bot',
		version='1.1.0',
		url='https://github.com/xlanor/CryptoKitties/',
		license='MIT',
		author='xlanor',
		author_email='tanjingkai@me.com',
		description='A telegram scanner for CryptoKitties',
		long_description='Alerting users based on the parameters given to the bot via telegram.',
		packages=find_packages(),
		include_package_data=True,
		zip_safe=False,
		platforms='any',
		install_requires=requires,
		dependency_links=links
	)