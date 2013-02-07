"""
Tests for turning a Tiddler into HTML within a TiddlyWiki document
"""

from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.serializer import Serializer
from tiddlyweb.config import config

from tiddlywebwiki.serialization import SPLITTER


BASE_TIDDLYWIKI = 'tiddlywebwiki/resources/empty.html'
config['base_tiddlywiki'] = BASE_TIDDLYWIKI
environ = {'tiddlyweb.config': config}


def test_html_attribute_escape_with_recipe():
    tiddler = Tiddler(
            'escape "double" quotes & &amp; in <tiddler> field values')
    tiddler.bag = 'foo "bar" baz'
    tiddler.recipe = 'baz "bar" foo'
    tiddler.modifier = 'Chris "sensei" Dent'
    tiddler.tags = ["foo", 'xxx "yyy" zzz']
    tiddler.fields["custom"] = u"""lorem 'ipsum' dolor "sit" amet"""
    tiddler.text = ''
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()

    assert ('title="escape &quot;double&quot; quotes &amp; '
        '&amp;amp; in &lt;tiddler&gt; field values"' in string)
    assert ('server.title="escape &quot;double&quot; quotes &amp; '
        '&amp;amp; in &lt;tiddler&gt; field values"' in string)
    assert 'bag="foo &quot;bar&quot; baz"' in string
    assert 'recipe="baz &quot;bar&quot; foo"' in string
    assert 'server.workspace="bags/foo &quot;bar&quot; baz"' in string
    assert 'modifier="Chris &quot;sensei&quot; Dent"' in string
    assert 'creator="Chris &quot;sensei&quot; Dent"' in string
    assert 'tags="foo [[xxx &quot;yyy&quot; zzz]]"' in string
    assert '''custom="lorem 'ipsum' dolor &quot;sit&quot; amet"''' in string
    # single tiddler's browse link is that tiddler in its bag
    assert ('you may still <a href="/bags/foo%20%22bar%22%20baz/tiddlers'
            '/escape%20%22double%22%20quotes%20%26%20%26amp%3B%20in%20%3C'
            'tiddler%3E%20field%20values">browse' in string)


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

    assert ('title="escape &quot;double&quot; quotes in tiddler field values"'
        in string)
    assert ('server.title="escape &quot;double&quot; quotes in tiddler '
        'field values"' in string)
    assert 'bag="foo &quot;bar&quot; baz"' in string
    assert 'server.workspace="bags/foo &quot;bar&quot; baz"' in string
    assert 'modifier="Chris &quot;sensei&quot; Dent"' in string
    assert 'creator="Chris &quot;sensei&quot; Dent"' in string
    assert 'tags="foo [[xxx &quot;yyy&quot; zzz]]"' in string
    assert '''custom="lorem 'ipsum' dolor &quot;sit&quot; amet"''' in string
    # single tiddler's browse link is that tiddler in its bag
    assert ('you may still <a href="/bags/foo%20%22bar%22%20baz/tiddlers/'
            'escape%20%22double%22%20quotes%20in%20tiddler%20field%20'
            'values">browse' in string)


def test_content_type():
    tiddler = Tiddler('Foo', 'Alpha')
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Foo', string)

    assert 'server.content-type=""' in tiddler

    tiddler = Tiddler('_Foo', 'Alpha')
    # possible weirdness in the text serialization and some stores
    # with empty type field being set to a string
    tiddler.type = 'None'
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('_Foo', string)

    assert 'server.content-type=""' in tiddler

    tiddler = Tiddler('Bar', 'Bravo')
    tiddler.type = 'text/x-custom'
    tiddler.text = 'lorem ipsum dolor sit amet'
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Bar', string)

    assert 'server.content-type="text/x-custom"' in tiddler
    assert '<pre>lorem ipsum dolor sit amet</pre>' in tiddler

    tiddler = Tiddler('Baz', 'Charlie')
    tiddler.type = 'application/x-custom'
    tiddler.text = 'lorem ipsum dolor sit amet'
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Baz', string)

    assert 'server.content-type="application/x-custom"' in tiddler


def test_server_etag():
    tiddler = Tiddler('Foo', 'Alpha')
    serializer = Serializer('tiddlywebwiki.serialization', environ)
    serializer.object = tiddler
    string = serializer.to_string()
    tiddler = _extract_tiddler('Foo', string)

    assert 'server.etag="&quot;Alpha/Foo/' in tiddler


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
