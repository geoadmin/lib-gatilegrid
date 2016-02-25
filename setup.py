from setuptools import setup, find_packages



setup(name='poolmanager',
      version='0.0.1',
      description='Geoadmin custom tile grid for web mapping applications',
      classifiers=[],
      keywords='',
      author='Loic Gasser',
      author_email='loicgasser4@gmail.com',
      license='MIT',
      url='https://github.com/loicgasser/gatilegrid',
      packages=find_packages(exclude=['tests']),
      package_dir={'gatilegrid': 'gatilegrid'},
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=[],
      )
      

