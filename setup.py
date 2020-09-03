# -*- coding: utf-8 -*-

# HACK for `nose.collector` to work on python 2.7.3 and earlier
import multiprocessing
import os
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='gatilegrid',
      version='0.2.0',
      description='Popular tile grids and grids API for web mapping applications',
      keywords='gis wmts grid map',
      author='Loic Gasser',
      author_email='loicgasser4@gmail.com',
      license='MIT',
      url='https://github.com/geoadmin/lib-gatilegrid',
      packages=['gatilegrid'],
      package_dir={'gatilegrid': 'gatilegrid'},
      include_package_data=True,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Scientific/Engineering :: GIS',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown',
      test_suite='nose.collector',
      install_requires=['future'],
      python_requires='>2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
      )
