import re
from codecs import open

from setuptools import setup

# Package information
AUTHOR = "Damego"
AUTHOR_EMAIL = "damego.dev@gmail.com"
DESCRIPTION = "Add localization support to your interactions.py bot"
PROJECT_NAME = "interactions-i18n"
MAIN_PACKAGE_NAME = "interactions.ext.i18n"
URL = "https://github.com/Damego/interactions-i18n"

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

with open("interactions/ext/i18n/base.py") as fp:
    VERSION = re.search('__version__ = "([^"]+)"', fp.read())[1]

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    include_package_data=True,
    install_requires=["discord-py-interactions>=4.3.2"],
    license="MIT License",
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    packages=["interactions.ext.i18n"],
    python_requires=">=3.8.6",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
