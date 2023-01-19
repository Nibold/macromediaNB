import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
name = "macromediaNB",
version = "0.1",
author = "Nicole Boldyrev",
author_email = "nboldyrev@stud.macromedia.de",
description = "Eine kleine 4 gewinnt package",
long_description = long_description,
long_description_content_type = "text/markdown",
url = "https://github.com/user0000/macromediaNB",
project_urls = {
    "Bug Tracker": "https://github.com/user0000/macromediaNB/issues",
},
license='MIT',
packages=['macromediaNB'],
install_requires=['requests'],
)