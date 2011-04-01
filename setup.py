# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import os.path
from setuptools import setup, find_packages


def read(*path):
    return open(os.path.join(*path)).read() + '\n\n'

setup(
    name='nagios.zopetestrunner',
    version='1.0dev',
    author='gocept',
    author_email='mail@gocept.com',
    description='A Nagios plugin that wraps the Zope testrunner.',
    long_description = (
        read('README.txt') +
        '.. contents::\n\n' +
        read('CHANGES.txt')
        ),
    url='http://pypi.python.org/pypi/nagios.zopetestrunner',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='ZPL 2.1',
    namespace_packages=['nagios'],
    entry_points="""
        [console_scripts]
        check_zopetestrunner = nagios.zopetestrunner.plugin:main
    """,
    install_requires=[
        'setuptools',
        'nagiosplugin',
        'zope.testrunner'
        ])
