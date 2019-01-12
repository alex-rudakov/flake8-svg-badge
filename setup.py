#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://flake8-svg-badge.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='flake8-svg-badge',
    version='0.1.0',
    description='Svg badge that shows % of problem-free code',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Alex Rudakov',
    author_email='ribozz@gmail.com',
    url='https://github.com/ribozz/flake8-svg-badge',
    packages=[
        'flake8_svg_badge',
    ],
    package_dir={'flake8_svg_badge': 'flake8_svg_badge'},
    include_package_data=True,
    install_requires=[
        "flake8 > 3.0.0",
    ],
    license='MIT',
    zip_safe=False,
    keywords='flake8-svg-badge',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    entry_points={
        'flake8.report': [
            'svg = flake8_svg_badge.reporter:ReportSVGBadge',
        ],
    },
)
