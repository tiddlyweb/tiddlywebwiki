import sys
import os

from tiddlyweb.model.bag import Bag
from tiddlyweb.store import Store
from tiddlyweb.manage import make_command, usage

from tiddlywebwiki.tiddlywiki import import_wiki_file
from tiddlywebwiki.instancer import update_instance
from tiddlywebwiki.importer import import_list


def init(config_in):
    global config
    config = config_in


@make_command()
def update(args):
    """Update all instance_tiddlers in the current instance."""
    update_instance(config)


@make_command()
def twimport(args):
    """Import one or more plugins, tiddlers or recipes in Cook format: <bag> <URI>"""
    bag = args[0]
    urls = args[1:]
    if not bag or not urls:
        raise IndexError('missing args')
    import_list(bag, urls)


@make_command()
def imwiki(args):
    """Import tiddlers from a Tiddlywiki document into a bag: <bag> <filename>"""
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
            environ={'tiddlyweb.config': config})
