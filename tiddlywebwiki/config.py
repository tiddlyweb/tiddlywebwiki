"""
Configuration additions for TiddlyWebWiki.

base_tiddlywiki: the file location of the tiddlywiki file into which
Tiddlers are pushed when creating outgoing TiddlyWiki representations
from TiddlyWeb. This can be an absolute path or relative to the startup
directory of the server.
"""

try:
    from pkg_resources import resource_filename
except ImportError:
    from tiddlywebplugins.utils import resource_filename


PACKAGE_NAME = 'tiddlywebwiki'
BASE_TIDDLYWIKI = resource_filename(PACKAGE_NAME, 'resources/empty.html')


config = {
    'instance_pkgstores': ['tiddlywebplugins.console', PACKAGE_NAME],
    'base_tiddlywiki': BASE_TIDDLYWIKI,
    'extension_types': {
        'wiki': 'text/x-tiddlywiki',
    },
    'serializers': {
        'text/x-tiddlywiki': ['tiddlywebwiki.serialization',
            'text/html; charset=UTF-8'],
    },
    'wikitext.default_renderer': 'tiddlywebplugins.wikklytextrender',
    'wikitext.type_render_map': {
        'text/x-tiddlywiki': 'tiddlywebplugins.wikklytextrender',
    },
    'tiddlywebwiki.friendlywiki': True,
    'wsgi_server': 'tiddlywebwiki.serve'
}
