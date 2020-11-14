from setuptools import setup, find_packages
from os import path
import pathlib

CWD = pathlib.Path(__file__).parent
README = (CWD / "README.md").read_text()

setup(
    name="meistertask_cli",
    packages=find_packages(),
    entry_points={"console_scripts": ["meistertask = src.__main__:main"]},
    version='0.0.2',
    description="Command-line client for Meistertask",
    long_description=README,
    long_description_content_type='text/markdown',
    author="ablil",
    author_email="ablil@protonmail.com",
    license="MIT",
    url="https://github.com/ablil/meistertask-cli",
    install_requires=[
        "requests",
    ],
    python_requires=">=2.7",
)