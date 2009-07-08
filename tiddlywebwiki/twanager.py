
from tiddlyweb.manage import make_command, usage
from tiddlywebwiki.importer import import_wiki_file
from tiddlywebwiki.instancer import instance, _make_bag, _make_recipe

@make_command()
def imwiki(args):
    """Import a Tiddlywiki html file into a bag: <filename> <bag>"""
    store = _store()

    try:
        filename, bag_name = args[0:2]
        import_wiki_file(store, filename, bag_name)
    except IndexError, exc:
        print >> sys.stderr, "index error: %s" % exc
        usage()
    except ValueError, exc:
        print >> sys.stderr, "value error: %s" % exc
        usage()


@make_command()
def instance(args):
    """Create a tiddlyweb instance with default plugins in the named directory: <dir>"""
    instance(args)
    _make_bag('common')
    _make_recipe('default', bag_names + ['common'])


def _store():
    """Get our Store from config."""
    return Store(config['server_store'][0],
            environ={'tiddlyweb.config': config})

def init(config_in):
    global config
    config = config_in
