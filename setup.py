from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='gatilegrid',
      version='1.0.0',
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
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Programming Language :: Python :: 3.13',
            'Topic :: Scientific/Engineering :: GIS',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=[],
      python_requires='>=3.10',
      )
