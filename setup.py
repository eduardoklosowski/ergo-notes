# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


version = __import__('ergonotes').__version__
with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')


setup(
    name='ergo-notes',
    version=version,
    packages=find_packages(),

    install_requires=['docutils'],

    author='Eduardo Augusto Klosowski',
    author_email='eduardo_klosowski@yahoo.com',

    description='Notes for Ergo',
    long_description=long_description,
    license='MIT',
    url='https://github.com/eduardoklosowski/ergo-notes',

    include_package_data=True,
    zip_safe=False,
)
