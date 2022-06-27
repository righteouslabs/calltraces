"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from importlib.metadata import version
from setuptools import setup, find_packages
import pathlib
import datetime
import requests
from requests.structures import CaseInsensitiveDict

here = pathlib.Path(__file__).parent.resolve()

# Get the version number from the datetime and previous versions

url = "https://test.pypi.org/pypi/calltraces/json"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

response = requests.get(url, headers=headers).status_code

version_number_prefix = datetime.datetime.now().strftime("%Y.%m.%d")
version_number_suffix = 0

while response == 200:
    url_prefix = "https://test.pypi.org/pypi/calltraces/"
    url_suffix = "/".join([(".".join([version_number_prefix, str(version_number_suffix)])), "json"])
    response = requests.get(url_prefix + url_suffix, headers=headers).status_code
    version_number = ".".join([version_number_prefix, str(version_number_suffix)])
    version_number_suffix += 1

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="calltraces",
    version=version_number,
    description="A small package for tracing function calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/righteouslabs/calltraces",
    author="Righteous AI Inc.",
    author_email="admin@righteous.ai",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "calltraces"},
    packages=find_packages(where="calltraces"),
    python_requires=">=3.9",
    project_urls={
        "Bug Reports": "https://github.com/righteouslabs/calltraces/issues",
        "Source": "https://github.com/righteouslabs/calltraces/",
    },
)