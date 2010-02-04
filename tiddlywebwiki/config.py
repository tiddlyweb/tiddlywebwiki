"""
Configuration additions for TiddlyWebWiki.

base_tiddlywiki: the file location of the tiddlywiki file into which
Tiddlers are pushed when creating outgoing TiddlyWiki representations
from TiddlyWeb. This can be an absolute path or relative to the startup
directory of the server.
"""

from tiddlywebplugins.instancer.util import get_tiddler_locations

from tiddlywebwiki.instance import store_contents

try:
    from pkg_resources import resource_filename
except ImportError:
    from tiddlywebplugins.utils import resource_filename


PACKAGE_NAME = 'tiddlywebwiki'
BASE_TIDDLYWIKI = resource_filename(PACKAGE_NAME, 'resources/empty.html')


config = {
    'instance_tiddlers': get_tiddler_locations(store_contents, PACKAGE_NAME),
    'base_tiddlywiki': BASE_TIDDLYWIKI,
    'extension_types': {
        'wiki': 'text/x-tiddlywiki',
        },
    'serializers': {
        'text/x-tiddlywiki': ['tiddlywebwiki.serialization',
            'text/html; charset=UTF-8'],
        },
    'wikitext.default_renderer': 'tiddlywebplugins.wikklytextrender',
    # XXX the following is, in most cases, redundant
    'wikitext.type_render_map': {
        'text/x-tiddlywiki': 'tiddlywebplugins.wikklytextrender',
        }
    }
