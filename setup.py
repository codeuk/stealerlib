#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @author:  codeuk
    @package: setup.py
"""

from distutils.core import setup

setup(
  name = 'StealerLib',
  packages = ['StealerLib'],
  version = '0.0.1',
  license='MIT',
  description = 'Python Information Stealer Library (for Windows)',
  author = 'Max D.',
  author_email = 'md54@gchq.agency',
  url = 'https://github.com/codeuk/stealerlib',
  keywords = ['INFORMATION', 'STEALER', 'AUTOMATION'],
  install_requires=[
          'psutil',
          'requests',
          'WMI',
          'pypiwin32',
          'pycryptodome',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
  ],
)