from setuptools import setup, find_packages
from os import path


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


setup(
    version='0.8',
    packages=find_packages(where='backend'),
    install_requires=['flask',
                      'flask_sqlalchemy',
                      'flask_bcrypt',
                      'flask-redis',
                      'flask-script',
                      'green',
                      'tox',
                      'pytest']
)
