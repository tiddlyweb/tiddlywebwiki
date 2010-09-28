
from tiddlywebplugins.twimport import import_one
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.collections import Tiddlers
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import Store
from tiddlyweb.serializer import Serializer
from tiddlyweb.config import config
from tiddlywebwiki.config import config as twwconfig
from tiddlyweb.util import merge_config
from tiddlyweb.control import get_tiddlers_from_bag

merge_config(config, twwconfig)

IMAGE = 'test/data/peermore.png'
ZERO = 'test/data/zero.bin'
HTML = 'test/data/index.html'

def setup_module(module):
    bag = Bag('holder')
    store = Store(config['server_store'][0], config['server_store'][1],
            {'tiddlyweb.config': config})
    store.put(bag)

    import_one('holder', IMAGE, store)
    import_one('holder', ZERO, store)

    tiddler = Tiddler('index', 'holder')
    tiddler.text = open(HTML).read().decode('UTF-8')
    tiddler.type = 'text/html'
    store.put(tiddler)
    module.store = store


def test_content_type():
    bag = Bag('holder')
    bag = store.get(bag)
    tiddlers = Tiddlers(store=store)
    for tiddler in store.list_bag_tiddlers(bag):
        tiddlers.add(tiddler)

    serializer = Serializer('tiddlywebwiki.serialization', {'tiddlyweb.config': config})
    output = ''.join(serializer.list_tiddlers(tiddlers))

    # we are expecting an img link to the image tiddler
    assert 'server.content-type="image/png"' in output

    # but we want just an html anchor link to the zero
    assert 'server.content-type="application/octet-stream"' in output

    assert 'server.content-type="text/html"' in output

def test_does_base64():
    serializer = Serializer('tiddlywebwiki.serialization',
            {'tiddlyweb.config': config})
    output = {}
    for title in ['index', 'peermore.png', 'zero.bin']:
        tiddler = store.get(Tiddler(title, 'holder'))
        output[tiddler.title] = serializer.serialization._tiddler_as_div(tiddler)

    assert '&lt;' in output['index']
    assert 'I=</pre>' in output['peermore.png']
    assert 'A==</pre>' in output['zero.bin']

def test_does_sizelimit():
    config['tiddlywebwiki.binary_limit'] = 200 # bytes
    serializer = Serializer('tiddlywebwiki.serialization',
            {'tiddlyweb.config': config})
    output = {}
    for title in ['index', 'peermore.png', 'zero.bin']:
        tiddler = store.get(Tiddler(title, 'holder'))
        output[tiddler.title] = serializer.serialization._tiddler_as_div(tiddler)

    assert '&lt;' in output['index']
    assert 'img src=' in output['peermore.png']
    assert 'a href=' not in output['peermore.png']
    assert 'bags/holder/tiddlers/peermore.png' in output['peermore.png']
    assert 'a href=' in output['zero.bin']
    assert 'img src=' not in output['zero.bin']
    assert 'bags/holder/tiddlers/zero.bin' in output['zero.bin']
