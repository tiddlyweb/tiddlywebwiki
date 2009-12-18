"""
A TiddlyWeb plugin providing a multi-user TiddlyWiki environment.
"""

__version__ = '0.20.2'


def init(config):
    # These imports must be in init otherwise getting
    # the version number causes cyclic imports to happen.
    import tiddlywebwiki.manage
    import tiddlywebplugins.status
    import tiddlywebplugins.atom
    import tiddlywebplugins.differ
    from tiddlyweb.util import merge_config
    from tiddlywebwiki.config import config as twwconfig

    merge_config(config, twwconfig)
    tiddlywebwiki.manage.init(config)
    tiddlywebplugins.status.init(config)
    tiddlywebplugins.atom.init(config)
    tiddlywebplugins.differ.init(config)
