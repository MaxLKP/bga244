from setuptools import setup, find_packages
from os import path

setup(
    name = "bga244",
    version = "0.1",
    author = 'Max K.',
    description = "Python serial interface for BGA244 Binary Gas Analyzer",
    url = 'https://github.com/MaxLKP/bga244',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    package_data = {"": ["*.yaml"], "": ["*.txt"]},
    install_requires = ['pyserial', 'pyyaml', 'pandas'],
    #scripts = [path.join("bga244", "bga244", "bga244_examples.py")]
)
