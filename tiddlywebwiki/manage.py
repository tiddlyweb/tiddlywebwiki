"""
TiddlyWebWiki-specific twanager commands
"""

from tiddlyweb.store import Store
from tiddlyweb.manage import make_command, usage


def init(config):

    @make_command()
    def update(args):
        """Update all instance_tiddlers in the current instance."""
        from tiddlywebplugins.instancer import Instance
        instance = Instance('.', config)
        instance.update_store()
