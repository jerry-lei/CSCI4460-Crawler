from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

setup(
    name='CSCI4460-Crawler',
    version='0.0.1',
    packages=find_packages(exclude=['doc', 'tests']),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
