"""
Configuration additions for tiddlywebwiki.

base_tiddlywiki -- the file location of the tiddlywiki
file into which Tiddlers are pushed when creating
outgoing TiddlyWiki representations from TiddlyWeb. This
can be an absolute path or relative to the startup
directory of the server.
"""

import os


CLIENT_PLUGIN_NAMES = [
    'TiddlyWebAdaptor.js',
    'ServerSideSavingPlugin.js',
    'TiddlyWebConfig.js',
    'RevisionsCommandPlugin.js',
    'DiffFormatterPlugin.js']


# determine file paths
try:
    from pkg_resources import resource_filename
    BASE_TIDDLYWIKI = resource_filename('tiddlywebwiki', 'empty.html')
    CLIENT_PLUGINS = ['file:%s' % resource_filename('tiddlywebwiki', plugin)
            for plugin in CLIENT_PLUGIN_NAMES]
    # The following list comprehension is required to make sure the meta
    # files get unpacked into the egg cache.
    ['file:%s' % resource_filename('tiddlywebwiki', '%s.meta' % plugin)
            for plugin in CLIENT_PLUGIN_NAMES]
except ImportError:
    BASE_TIDDLYWIKI = os.path.join('tiddlywebwiki', 'empty.html')
    CLIENT_PLUGINS = ['file:%s' % os.path.join('tiddlywebwiki', plugin)
        for plugin in CLIENT_PLUGIN_NAMES]


config = {
        'base_tiddlywiki': BASE_TIDDLYWIKI,
        'instance_tiddlers': {
            'system': CLIENT_PLUGINS
            },
        'extension_types': {
            'wiki': 'text/x-tiddlywiki',
            },
        'serializers': {
            'text/x-tiddlywiki': ['tiddlywebwiki.serialization', 'text/html; charset=UTF-8'],
            },
        'wikitext.default_renderer': 'tiddlywebplugins.wikklytextrender',
        # XXX the following is, in most cases, redundant
        'wikitext.type_render_map': {
            'text/x-tiddlywiki': 'tiddlywebplugins.wikklytextrender',
            }
        }
