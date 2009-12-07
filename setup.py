from setuptools import setup, find_packages

from tiddlywebwiki import __version__ as VERSION


setup(name = 'tiddlywebwiki',
        version = VERSION,
        description = 'A TiddlyWeb plugin to provide a multi-user TiddlyWiki environment.',
        author = 'FND',
        author_email = 'FNDo@gmx.net',
        packages = find_packages(exclude=['test']),
        py_modules = ['differ'],
        scripts = ['twinstance'],
        platforms = 'Posix; MacOS X; Windows',
        install_requires = ['tiddlyweb>=0.9.79',
            'tiddlywebplugins.wikklytextrender',
            'tiddlywebplugins.status',
            'tiddlywebplugins.atom',
            'tiddlywebplugins.utils',
            'BeautifulSoup',
            'wikklytext'],
        include_package_data = True,
        )
