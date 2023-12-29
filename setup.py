#!/usr/bin/env python3
from setuptools import setup
# from distutils.core import setup
with open('README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(
  name = 'lambdaorm',
  packages = ['lambdaorm'],
  version = '0.0.1',
  description = 'LambdaORM Client for Python',
  long_description=long_description,
  long_description_content_type='text/markdown',  # This is important!
  url = 'https://github.com/lambda-orm/lambdaorm-client-kotlin', # use the URL to the GitHub repo
  download_url = 'https://github.com/lambda-orm/lambdaorm-client-kotlin/tarball/0.0.1',
  keywords = ['orm', 'lambdaorm', 'lambda', 'orm-client', 'orm-client-python'],
  classifiers = [],
  author = 'Flavio Lionel Rita',
  author_email = 'flaviolrita@proton.me'
)