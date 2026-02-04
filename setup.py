from setuptools import setup, find_packages

setup(
    name = "bga244",
    version = "0.1",
    author = 'Max K.',
    description = "Python serial interface for BGA244 Binary Gas Analyzer",
    url = 'https://github.com/MaxLKP/bga244',
    license = 'MIT',
    packages = find_packages(),
    package_data = {"bga244": ["gas_config/*.xlsx", "gas_config/*.txt", "gas_config/*.yaml"]},
    install_requires = ['pyserial', 'pyyaml']
)
