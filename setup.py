# Always prefer setuptools over distutils
# To use a consistent encoding
from codecs import open
from os import path

import setuptools


setuptools.setup(
    name="msgraph_outlook",
    project_name="msgraph_outlook",
    version="0.0.1",
    author="Ryan Cope",
    author_email="<ryancopedev@gmail.com",
    description="<Template Setup.py package>",
    long_description="MSGraph Outlook Package",
    long_description_content_type="text/markdown",
    url="<https://github.com/authorname/templatepackage>",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
