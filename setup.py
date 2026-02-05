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
    package_data = {"bga244": [path.join("bga244", "gas_config", "bga244_gases.xlsx"), path.join("bga244", "gas_config", "gaes.txt"), path.join("bga244", "gas_config", "gases.yaml"), path.join("bga244", "gas_config", "cas_nr.txt")]},
    install_requires = ['pyserial', 'pyyaml', 'pandas'],
    #scripts = [path.join("bga244", "bga244", "bga244_examples.py")]
)
