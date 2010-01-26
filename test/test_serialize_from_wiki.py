
from tiddlyweb.model.bag import Bag
from tiddlyweb.serializer import Serializer

WIKI = 'test/data/wiki.html'

def test_from_wiki():
    bag = Bag('fromwiki')
    serializer = Serializer('tiddlywebwiki.serialization')
    serializer.object = bag

    tiddlers = bag.list_tiddlers()
    assert len(tiddlers) == 0

    wiki_string = open(WIKI).read()

    bag = serializer.from_string(wiki_string)

    tiddlers = bag.list_tiddlers()

    assert len(tiddlers) == 2
    assert 'RESTBasics' in [tiddler.title for tiddler in tiddlers]


