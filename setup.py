"""A setuptools based general setup module for PyPI.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from importlib.metadata import version
from unicodedata import name
from setuptools import setup, find_packages
import pathlib
import datetime
import requests
from requests.structures import CaseInsensitiveDict
import sys, getopt

here = pathlib.Path(__file__).parent.resolve()

# Get the host and project name from the command line arguments
argv = sys.argv[1:]
try:
    options, arguments = getopt.getopt(argv, "h:n:", ["host=", "name="])
except getopt.GetoptError:
    print(
        "Invalid usage, please use the syntax: setup.py -h <host> -n <name> or setup.py --host <host> --name <name>"
    )
    sys.exit(2)
for opt, arg in options:
    if opt in ("-h", "--host"):
        host = arg
    elif opt in ("-n", "--name"):
        project_name = arg

# Get the version number from the datetime and previous versions
url = "https://" + host + "/pypi/" + project_name + "/json"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

response = requests.get(url, headers=headers).status_code

version_number_prefix = datetime.datetime.now().strftime("%Y.%m.%d")
version_number_suffix = 0

while response == 200:
    url = (
        "https://"
        + host
        + "/pypi/"
        + project_name
        + "/"
        + version_number_prefix
        + "."
        + str(version_number_suffix)
        + "/json"
    )
    response = requests.get(url, headers=headers).status_code
    version_number = version_number_prefix + "." + str(version_number_suffix)
    version_number_suffix += 1

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name=project_name,
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
    package_dir={"": project_name},
    packages=find_packages(where=project_name),
    python_requires=">=3.9",
    project_urls={
        "Bug Reports": "https://github.com/righteouslabs/calltraces/issues",
        "Source": "https://github.com/righteouslabs/calltraces/",
    },
)
