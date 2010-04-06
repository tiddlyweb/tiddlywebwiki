"""
Tests for turning a Tiddler into HTML within a TiddlyWiki document
"""

from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.serializer import Serializer
from tiddlyweb.config import config

from tiddlywebwiki.serialization import SPLITTER


# TODO: use module_setup!?
BASE_TIDDLYWIKI = 'tiddlywebwiki/resources/empty.html'
config['base_tiddlywiki'] = BASE_TIDDLYWIKI
environ = { 'tiddlyweb.config': config }


def test_html_attribute_escape_with_recipe():
    tiddler = Tiddler('escape "double" quotes in tiddler field values')
    tiddler.bag = 'foo "bar" baz'
    tiddler.recipe = 'baz "bar" foo'
    tiddler.modifier = 'Chris "sensei" Dent'
    tiddler.tags = ["foo", 'xxx "yyy" zzz']
    tiddler.fields["custom"] = u"""lorem 'ipsum' dolor "sit" amet"""
    tiddler.text = ''
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()

    assert r'''title="escape &quot;double&quot; quotes in tiddler field values"''' in string
    assert r'''server.title="escape &quot;double&quot; quotes in tiddler field values"''' in string
    assert r'''bag="foo &quot;bar&quot; baz"''' in string
    assert r'''recipe="baz &quot;bar&quot; foo"''' in string
    assert r'''server.workspace="bags/foo &quot;bar&quot; baz"''' in string
    assert r'''modifier="Chris &quot;sensei&quot; Dent"''' in string
    assert r'''creator="Chris &quot;sensei&quot; Dent"''' in string
    assert r'''tags="foo [[xxx &quot;yyy&quot; zzz]]"''' in string
    assert r'''custom="lorem 'ipsum' dolor &quot;sit&quot; amet"''' in string
    assert r'''you may still <a href="http://0.0.0.0:8080/recipes/baz%20%22bar%22%20foo/tiddlers">browse''' in string


def test_html_attribute_escape_with_bag():
    tiddler = Tiddler('escape "double" quotes in tiddler field values')
    tiddler.bag = 'foo "bar" baz'
    tiddler.modifier = 'Chris "sensei" Dent'
    tiddler.tags = ["foo", 'xxx "yyy" zzz']
    tiddler.fields["custom"] = u"""lorem 'ipsum' dolor "sit" amet"""
    tiddler.text = ''
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()

    assert r'''title="escape &quot;double&quot; quotes in tiddler field values"''' in string
    assert r'''server.title="escape &quot;double&quot; quotes in tiddler field values"''' in string
    assert r'''bag="foo &quot;bar&quot; baz"''' in string
    assert r'''server.workspace="bags/foo &quot;bar&quot; baz"''' in string
    assert r'''modifier="Chris &quot;sensei&quot; Dent"''' in string
    assert r'''creator="Chris &quot;sensei&quot; Dent"''' in string
    assert r'''tags="foo [[xxx &quot;yyy&quot; zzz]]"''' in string
    assert r'''custom="lorem 'ipsum' dolor &quot;sit&quot; amet"''' in string
    assert r'''you may still <a href="http://0.0.0.0:8080/bags/foo%20%22bar%22%20baz/tiddlers">browse''' in string


def test_content_type():
    tiddler = Tiddler('Foo', 'Alpha')
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Foo', string)

    assert r'''server.content-type=""''' in tiddler

    tiddler = Tiddler('Bar', 'Bravo')
    tiddler.type = 'text/x-custom'
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Bar', string)

    assert r'''server.content-type="text/x-custom"''' in tiddler

    tiddler = Tiddler('Baz', 'Charlie')
    tiddler.type = 'None' # possible weirdness in the text serialization and some stores
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Baz', string)

    assert r'''server.content-type=""''' in tiddler


def _extract_tiddler(title, wiki):
    """
    helper function to extract a tiddler DIV from a TiddlyWiki string

    tiddlywebplugins.twimport:wiki_string_to_tiddlers does this better
    """
    tiddlystart, tiddlyfinish = wiki.split(SPLITTER, 2)
    tiddlystart, store = tiddlystart.split('<div id="storeArea">', 2)
    splitter = '<div title='
    for tiddler in store.split(splitter):
        if tiddler.startswith('"%s"' % title):
            return splitter + tiddler
