from setuptools import setup, find_packages

requirements = ['numpy>=1.19.4', 'pandas>=1.1.5', 'open3d>=0.11.2', 'laspy>=1.7.0']

setup(name="point_cloud_io",
      packages=find_packages(),
      install_requires=requirements,
      version="0.0.1",
      author="Nicholas Arnold",
      author_email="n.arnold@lancaster.ac.uk",
      python_requires='>=3.8',
      )
