
from tiddlywebplugins.twimport import import_one
from tiddlyweb.model.bag import Bag
from tiddlyweb.store import Store
from tiddlyweb.serializer import Serializer
from tiddlyweb.config import config
from tiddlywebwiki.config import config as twwconfig
from tiddlyweb.util import merge_config
from tiddlyweb.control import get_tiddlers_from_bag

merge_config(config, twwconfig)

IMAGE = 'test/data/peermore.png'
ZERO = 'test/data/zero.bin'

def setup_module(module):
    bag = Bag('holder')
    store = Store(config['server_store'][0], config['server_store'][1],
            {'tiddlyweb.config': config})
    store.put(bag)

    import_one('holder', IMAGE, store)
    import_one('holder', ZERO, store)
    module.store = store


def test_serialize_binary():
    bag = Bag('holder')
    bag = store.get(bag)
    tmpbag = Bag('tmpbag', tmpbag=True)
    tmpbag.add_tiddlers(get_tiddlers_from_bag(bag))

    serializer = Serializer('tiddlywebwiki.serialization', {'tiddlyweb.config': config})
    output = ''.join(serializer.list_tiddlers(tmpbag))

    # we are expecting an img link to the image tiddler
    assert 'server.content-type="image/png"' in output

    # but we want just an html anchor link to the zero
    assert 'server.content-type="application/octet-stream"' in output
