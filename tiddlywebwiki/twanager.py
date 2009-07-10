from tiddlyweb.model.bag import Bag
from tiddlyweb.manage import make_command, usage
from tiddlywebwiki.importer import import_wiki_file
from tiddlywebwiki.instancer import instance as create_instance
from tiddlywebwiki.instancer import _store_bag, _make_recipe, _generate_secret


@make_command()
def imwiki(args):
    """Import tiddlers from a Tiddlywiki document into a bag: <filename> <bag>"""
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
    """Create a TiddlyWebWiki instance in the given directory: <dir>"""
    config = {
        'system_plugins': ['tiddlywebwiki.plugin'],
        'twanager_plugins': ['tiddlywebwiki.plugin']
    }
    create_instance(args, config=config)

    bag = Bag('system')
    bag.policy.write = ['R:ADMIN']
    bag.policy.create = ['R:ADMIN']
    bag.policy.delete = ['R:ADMIN']
    bag.policy.manage = ['R:ADMIN']
    bag.policy.accept = ['R:ADMIN']
    _store_bag(bag)

    bag = Bag('common')
    bag.policy.delete = ['R:ADMIN']
    _store_bag(bag)

    recipe = _make_recipe('default', ['system', 'common'])


def _store():
    """Get our Store from config."""
    return Store(config['server_store'][0],
            environ={'tiddlyweb.config': config})


def init(config_in):
    global config
    config = config_in