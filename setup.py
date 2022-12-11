"""
Created on 

@author: Jordy Rillaerts
"""

"""API_CLIENTS package setup script

   To create a source distribution of the API_CLIENTS package run

   python API_CLIENTS.py sdist

   which will create an archive file in the 'dist' subdirectory.
   The archive file will be  called 'API_CLIENTS-X.X.zip' and will
   unpack into a directory 'API_CLIENTS-X.X'.

   An end-user wishing to install the API_CLIENTS package can simply
   unpack 'API_CLIENTS-X.X.zip' and from the 'API_CLIENTS-X.X' directory and
   run

   python setup.py install

   which will ultimately copy the API_CLIENTS package to the appropriate
   directory for 3rd party modules in their Python installation

   To create an executable installer use the bdist_wininst command

   python setup.py bdist_wininst

   which will create an executable installer, 'API_CLIENTS-X.X.win32.exe',
   in the current directory.
"""

import setuptools


# package naming
DISTNAME = "API_Clients"

# descriptions
DESCRIPTION = f"{DISTNAME} contains all my code assisting in accessing various api"
with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# developer(s)
AUTHOR = "Jordy Rillaerts"
EMAIL = "jordy_rillaerts13@hotmail.com"

URL = "https://github.com/jordyril/API_CLIENTS"

# versioning
MAJOR = 1
MINOR = 0
MICRO = 1
ISRELEASED = False
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)

FULLVERSION = VERSION
write_version = True

# if not ISRELEASED:
# FULLVERSION += '.dev'


# DEPENDENCIES = []

# with open("requirements.txt", "r", encoding="utf-8") as requirements:
#     for line in requirements:
#         DEPENDENCIES.append(line.split("==")[0].strip())
#         # DEPENDENCIES.append(line.strip())

# DEPENDENCIES += ["musicbrainzngs", "nltk", "requests", "urllib", "pandas", "re", "os", "base64", "datetime"]

setuptools.setup(
    name=DISTNAME,
    version=FULLVERSION,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    # install_requires=DEPENDENCIES,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    long_description_content_type="test/markdown",
    packages=["API_Clients"],
)
