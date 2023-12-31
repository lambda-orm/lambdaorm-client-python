#!/usr/bin/env python3
from setuptools import setup
with open('README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='lambdaorm',
  packages=['lambdaorm'],
  version='0.0.2',
  license='MIT',
  description='LambdaORM Client for Python',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='Flavio Lionel Rita',
  author_email='flaviolrita@proton.me',
  url='https://github.com/lambda-orm/lambdaorm-client-kotlin',
  download_url='https://github.com/lambda-orm/lambdaorm-client-kotlin',
  keywords=['orm', 'lambdaorm', 'lambda', 'orm-client', 'orm-client-python'],
  install_requires=['dataclasses-json'],
  classifiers=[]
)