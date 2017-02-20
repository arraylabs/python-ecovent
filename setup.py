from setuptools import setup


with open('LICENSE') as f:
    license = f.read()

setup(
    name='python-ecovent',
    version='0.0.1',
    description='Python package for controlling local Ecovent Hub',
    author='Chris Campbell',
    author_email='chris@arraylabs.com',
    url='https://github.com/arraylabs/python-ecovent',
    license=license,
    packages=['ecovent'],
    package_dir={'ecovent': 'ecovent'}
)
