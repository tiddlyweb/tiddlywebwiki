"""
TiddlyWebWiki-specific twanager commands
"""

from tiddlyweb.store import Store
from tiddlyweb.manage import make_command, usage

from tiddlywebwiki.tiddlywiki import import_wiki_file
from tiddlywebwiki.importer import import_list


def init(config):

    @make_command()
    def update(args):
        """Update all instance_tiddlers in the current instance."""
        from tiddlywebplugins.instancer import Instance
        instance = Instance('.', config)
        instance.update_store()

    @make_command()
    def twimport(args):
        """Import one or more plugins, tiddlers or recipes in Cook format or a wiki: <bag> <URI>"""
        bag = args[0]
        urls = args[1:]
        if not bag or not urls:
            raise IndexError('missing args')
        import_list(bag, urls, config)

    @make_command()
    def imwiki(args):
        """Import tiddlers from a Tiddlywiki document into a bag, deprecated in favor of twimport: <bag> <filename>"""
        # XXX to be removed soon, deprecated.
        store = _store()

        try:
            bag_name, filename = args[0:2]
            import_wiki_file(store, filename, bag_name)
        except IndexError, exc:
            usage("index error: %s" % exc)
        except ValueError, exc:
            usage("value error: %s" % exc)

    def _store():
        """Get our Store from config."""
        return Store(config['server_store'][0],
                config['server_store'][1],
            environ={'tiddlyweb.config': config})
