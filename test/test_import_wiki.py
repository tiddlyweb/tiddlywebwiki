"""
Test some of the wiki importing routines.
"""

from tiddlywebwiki.tiddlywiki import import_wiki_file
from tiddlyweb.config import config
import tiddlywebwiki.manage

from tiddlyweb.model.bag import Bag
from tiddlyweb import control

def setup_module(module):
    tiddlywebwiki.manage.init(config)


def test_import_wiki_file():
    store = tiddlywebwiki.manage._store()
    bag = Bag('wiki')
    store.put(bag)

    import_wiki_file(store, filename='test/index.html')

    bag = store.get(bag)
    tiddlers = bag.list_tiddlers()

    assert len(tiddlers) == 191
    assert 'Osmosoft' in [tiddler.title for tiddler in tiddlers]
