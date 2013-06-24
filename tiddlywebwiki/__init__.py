"""
A TiddlyWeb plugin providing a multi-user TiddlyWiki environment.
"""

__version__ = '0.67.0'


def friendlywiki(environ, start_response):
    """
    Reframe the WSGI environment before internally redirecting
    to a recipe.
    """
    from tiddlyweb.web.handler.recipe import get_tiddlers
    environ['tiddlyweb.type'] = 'text/x-tiddlywiki'
    return get_tiddlers(environ, start_response)


def init(config):
    # These imports must be in init otherwise getting
    # the version number causes cyclic imports to happen.
    import tiddlywebplugins.imaker
    import tiddlywebplugins.status
    import tiddlywebplugins.atom
    import tiddlywebplugins.differ
    import tiddlywebplugins.console
    from tiddlyweb.util import merge_config
    from tiddlywebwiki.config import config as twwconfig

    merge_config(config, twwconfig)
    tiddlywebplugins.imaker.init(config)
    tiddlywebplugins.status.init(config)
    tiddlywebplugins.atom.init(config)
    tiddlywebplugins.differ.init(config)
    tiddlywebplugins.console.init(config)

    if 'selector' in config:
        if config.get('tiddlywebwiki.friendlywiki', True):
            config['selector'].add('/{recipe_name:segment}', GET=friendlywiki)
