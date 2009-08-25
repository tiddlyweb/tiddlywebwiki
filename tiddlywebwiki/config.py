"""
Configuration additions for tiddlywebwiki.

base_tiddlywiki -- the file location of the tiddlywiki
file into which Tiddlers are pushed when creating
outgoing TiddlyWiki representations from TiddlyWeb. This
can be an absolute path or relative to the startup
directory of the server.
"""

import os


try:
    from pkg_resources import resource_filename
    RESOURCES_DIRECTORY = resource_filename('tiddlywebwiki', 'empty.html') # XXX: hacky!?
    RESOURCES_DIRECTORY = os.path.dirname(RESOURCES_DIRECTORY)
except ImportError:
    RESOURCES_DIRECTORY = 'tiddlywebwiki'

BASE_TIDDLYWIKI = os.path.join(RESOURCES_DIRECTORY, 'empty.html')

CLIENT_PLUGINS = [
    'TiddlyWebAdaptor.js',
    'ServerSideSavingPlugin.js',
    'TiddlyWebConfig.js']
CLIENT_PLUGINS = [os.path.join(RESOURCES_DIRECTORY, plugin)
    for plugin in CLIENT_PLUGINS]

config = {
        'base_tiddlywiki': BASE_TIDDLYWIKI,
        'twanager_plugins': [
            'tiddlywebwiki.fromsvn',
            'tiddlywebwiki.instancer',
            'tiddlywebwiki.twanager'
            ],
        'instance_tiddlers': [
            ('system', CLIENT_PLUGINS),
            ],
        'extension_types': {
            'wiki': 'text/x-tiddlywiki',
            },
        'serializers': {
            'text/x-tiddlywiki': ['tiddlywebwiki.serialization', 'text/html; charset=UTF-8'],
            },
        'wikitext.default_renderer': 'wikklytextrender',
        # XXX the following is, in most cases, redundant
        'wikitext.type_render_map': {
            'text/x-tiddlywiki': 'wikklytextrender',
            }
        }
