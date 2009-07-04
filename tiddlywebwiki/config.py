"""
Configuration additions for tiddlywebwiki.

base_tiddlywiki -- the file location of the tiddlywiki
file into which Tiddlers are pushed when creating
outgoing TiddlyWiki representations from TiddlyWeb. This
can be an absolute path or relative to the startup 
directory of the server.

"""

try:
    from pkg_resources import resource_filename
    BASE_TIDDLYWIKI = resource_filename('tiddlywebwiki', 'empty.html')
except ImportError:
    BASE_TIDDLYWIKI = 'tiddlywebwiki/empty.html'

config = {
        'base_tiddlywiki': BASE_TIDDLYWIKI, 
        'instance_tiddlers': [
            ('system', [
                'http://svn.tiddlywiki.org/Trunk/association/adaptors/TiddlyWebAdaptor.js',
                'http://svn.tiddlywiki.org/Trunk/association/plugins/ServerSideSavingPlugin.js',
                'http://svn.tiddlywiki.org/Trunk/association/plugins/TiddlyWebConfig.js'
                ]),
            ],
        'extension_types': {
            'wiki': 'text/x-tiddlywiki',
            },
        'serializers': {
            'text/x-tiddlywiki': ['tiddlywebwiki.serialization', 'text/html; charset=UTF-8'],
            },
        'wikitext_renderer': 'wikklytextrender',
        'wikitext_render_map': {
            'text/x-tiddlywiki': 'wikklytextrender',
            },
        }
