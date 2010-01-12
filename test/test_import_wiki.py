"""
Test some of the wiki importing routines.
"""

import tiddlywebwiki.manage

from tiddlyweb.model.bag import Bag
from tiddlyweb.store import Store
from tiddlyweb import control
from tiddlyweb.config import config

from tiddlywebwiki.tiddlywiki import import_wiki_file


def setup_module(module):
    tiddlywebwiki.manage.init(config)


def test_import_wiki_file():
    store = _store()
    bag = Bag('wiki')
    store.put(bag)

    import_wiki_file(store, filename='test/index.html')

    bag = store.get(bag)
    tiddlers = bag.list_tiddlers()

    assert len(tiddlers) == 191
    assert 'Osmosoft' in [tiddler.title for tiddler in tiddlers]


def _store():
    """Get our Store from config."""
    return Store(config['server_store'][0],
            config['server_store'][1],
        environ={'tiddlyweb.config': config})
