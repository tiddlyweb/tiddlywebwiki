"""
TiddlyWebWiki-specific twanager commands
"""

from tiddlyweb.manage import make_command


def init(config):
    """
    Initialize the twanager commands.
    """

    @make_command()
    def update(args):
        """Update all instance_tiddlers in the current instance."""
        from tiddlywebplugins.instancer import Instance
        instance = Instance('.', config)
        instance.update_store()
