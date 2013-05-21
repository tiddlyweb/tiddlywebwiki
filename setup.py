from setuptools import setup, find_packages

from tiddlywebwiki import __version__ as VERSION


setup(
    name = 'tiddlywebwiki',
    version = VERSION,
    description = 'A TiddlyWeb plugin to provide a multi-user TiddlyWiki environment.',
    author = 'FND',
    author_email = 'FNDo@gmx.net',
    platforms = 'Posix; MacOS X; Windows',
    scripts = ['twinstance'],
    packages = find_packages(exclude=['test']),
    install_requires = [
        'tiddlyweb>=1.4.11',
        'tiddlywebplugins.imaker',
        'tiddlywebplugins.utils>=0.15',
        'tiddlywebplugins.wikklytextrender>=0.7',
        'tiddlywebplugins.status>=0.5',
        'tiddlywebplugins.differ',
        'tiddlywebplugins.atom',
        'tiddlywebplugins.console>=0.3.0',
        'cherrypy',
    ],
    include_package_data = True,
    zip_safe = False
)
