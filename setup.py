# -*- coding: utf-8 -*-

# HACK for `nose.collector` to work on python 2.7.3 and earlier
import multiprocessing
import os
from setuptools import setup


try:
    from pypandoc import convert
    README = convert('README.md', 'rst')
except ImportError:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


setup(name='gatilegrid',
      version='0.1.5',
      description='Popular tile grids and grids API for web mapping applications',
      classifiers=[],
      keywords='',
      author='Loic Gasser',
      author_email='loicgasser4@gmail.com',
      license='MIT',
      url='https://github.com/geoadmin/lib-gatilegrid',
      packages=['gatilegrid'],
      package_dir={'gatilegrid': 'gatilegrid'},
      include_package_data=True,
      zip_safe=False,
      long_description=README,
      test_suite='nose.collector',
      install_requires=['future'],
      )
