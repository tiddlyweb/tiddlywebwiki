from setuptools import setup, find_packages

from tiddlywebwiki import __version__ as VERSION


setup(
    name = 'tiddlywebwiki',
    version = VERSION,
    description = 'A TiddlyWeb plugin to provide a multi-user TiddlyWiki environment.',
    author = 'FND',
    author_email = 'FNDo@gmx.net',
    packages = find_packages(exclude=['test']),
    scripts = ['twinstance'],
    platforms = 'Posix; MacOS X; Windows',
    install_requires = [
        'tiddlyweb>=0.9.83',
        'tiddlywebplugins.wikklytextrender',
        'tiddlywebplugins.status>=0.5',
        'tiddlywebplugins.differ',
        'tiddlywebplugins.atom',
        'tiddlywebplugins.utils',
        'tiddlywebplugins.instancer>=0.5.5',
        'BeautifulSoup',
        'wikklytext'],
    include_package_data = True,
    zip_safe = False
    )
