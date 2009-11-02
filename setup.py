"""
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from tiddlywebwiki import __version__ as VERSION


setup(name = 'tiddlywebwiki',
        version = VERSION,
        description = 'A TiddlyWeb plugin to provide a multi-user TiddlyWiki environment.',
        author = 'Chris Dent',
        author_email = 'cdent@peermore.com',
        packages = ['tiddlywebwiki'],
        py_modules = ['differ'],
        scripts = ['twinstance'],
        platforms = 'Posix; MacOS X; Windows',
        install_requires = ['tiddlyweb', 'tiddlywebplugins.wikklytextrender', 'tiddlywebplugins.status', 'BeautifulSoup', 'wikklytext'],
        include_package_data = True,
        )
