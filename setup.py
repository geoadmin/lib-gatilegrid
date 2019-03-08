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
      version='0.1.11',
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
            'Topic :: Scientific/Engineering :: GIS',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
      zip_safe=False,
      long_description=README,
      test_suite='nose.collector',
      install_requires=['future'],
      )
