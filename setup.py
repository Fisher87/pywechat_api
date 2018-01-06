#!/usr/bin/env python
#coding=utf8

try:
    from  setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
        name='pywechat',
        version='1.0',
        description= 'BDTT company wechat spider api.',
        url = 'http://gitlab.benditoutiao.com/bdtt/pywechat', 
        author = 'bdtt_data_group',
        author_email = 'btdd@benditoutiao.com',
        classifiers=[ 'Programming Language :: Python :: 2.7',],
        include_package_data=True,
        packages = find_packages()
        )
