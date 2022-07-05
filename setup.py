# Always prefer setuptools over distutils
from setuptools import setup
import requests
import datetime
from requests.structures import CaseInsensitiveDict
import os


def get_version():
    # Defining the host and project name
    host = os.getenv("PYTHON_PACKAGE_HOST", "test.pypi.org")  # Default value set
    project_name = "calltraces"

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

    return version_number


if __name__ == "__main__":
    setup(
        version=get_version(),
        use_scm_version=True,
    )
