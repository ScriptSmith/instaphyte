#!/usr/bin/env python

from setuptools import setup

requirements = [
    "socialreaper",
    "tqdm==4.23.4"
]

setup(name='instaphyte',
      version='1.1.0',
      description='Simple Instagram hashtag and location scraper',
      author='Adam Smith',
      author_email='adam.smith1@uq.edu.au',
      url='https://github.com/scriptsmith/instaphyte',
      packages=["instaphyte"],
      python_requires=">=3.6",
      install_requires=requirements,
      package_dir={"instaphyte": "instaphyte"},
      entry_points={
          "console_scripts": ["instaphyte=instaphyte.cli:main"]
      },
      license="MIT",
      keywords=(['instagram', 'instagram-scraper', 'instagram-api',
                 'socialreaper'])
      )
