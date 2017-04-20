# -*- coding: utf-8 -*-

# HACK for `nose.collector` to work on python 2.7.3 and earlier
import multiprocessing
from setuptools import setup, find_packages



setup(name='gatilegrid',
      version='0.0.8',
      description='Popular tile grids and grids API for web mapping applications',
      classifiers=[],
      keywords='',
      author='Loic Gasser',
      author_email='loicgasser4@gmail.com',
      license='MIT',
      url='https://github.com/geoadmin/gatilegrid',
      packages=find_packages(exclude=['tests']),
      package_dir={'gatilegrid': 'gatilegrid'},
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=['future'],
      )
