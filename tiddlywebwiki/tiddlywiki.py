"""
Functionality for parsing TiddlyWiki documents.
"""

import codecs

import html5lib
from html5lib import treebuilders

from tiddlyweb.model.tiddler import Tiddler, string_to_tags_list


def import_wiki(environ, start_response):
    """
    Accept a tiddlywiki as POST and using it as the source
    parse it for tiddlers to be stored in the named bag.
    """
    bag_name = _determine_bag_name(environ)
    bag = _get_bag(environ, bag_name, True)
    length = environ['CONTENT_LENGTH']
    content = environ['wsgi.input'].read(int(length))

    bag.policy.allows(environ['tiddlyweb.usersign'], 'create')

    try:
        serialize_type, mime_type = web.get_serialize_type(environ)
        serializer = Serializer(serialize_type, environ)
        serializer.object = bag

        serializer.from_string(content)
    except NoSerializationError:
        raise HTTP415('Content type not supported: %s' % mime_type)
    except AttributeError, exc:
        raise HTTP400('Content malformed: %s' % exc)

    start_response("204 No Content",
            [('Location', '%s/tiddlers' % web.bag_url(environ, bag))])
    return ['']


def import_wiki_file(store, filename='wiki', bagname='wiki'):
    """
    Read a wiki in a file and import all the tiddlers into a bag.
    """
    wikifile = codecs.open(filename, encoding='utf-8', errors='replace')
    wikitext = wikifile.read()
    wikifile.close()
    return import_wiki(store, wikitext, bagname)


def import_wiki(store, wikitext, bagname='wiki'):
    """
    Import the wiki provided as a string and import all the tiddlers
    into a bag.
    """
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder('beautifulsoup'))
    soup = parser.parse(wikitext)
    store_area = soup.find('div', id='storeArea')
    divs = store_area.findAll('div')

    for tiddler_div in divs:
        handle_tiddler_div(bagname, tiddler_div, store)


def handle_tiddler_div(bagname, tiddler_div, store):
    """
    Create a new Tiddler from a tiddler div, in BeautifulSoup form.
    """
    tiddler = get_tiddler_from_div(tiddler_div)
    tiddler.bag = bagname
    try:
        store.put(tiddler)
    except OSError, exc:
        # This tiddler has a name that we can't yet write to the
        # store. For now we just state the error and carry on.
        import sys
        print >> sys.stderr, 'Unable to write %s: %s' % (tiddler.title, exc)


def get_tiddler_from_div(node):
    """
    Create a Tiddler from a BeautifulSoup DIV node
    """
    tiddler = Tiddler(node['title'])
    try:
        tiddler.text = _html_decode(node.find('pre').contents[0])
    except IndexError:
        # there are no contents in the tiddler
        tiddler.text = ''

    for attr, value in node.attrs:
        data = node.get(attr, None)
        if data and attr != 'tags':
            if attr in (['modifier', 'created', 'modified']):
                tiddler.__setattr__(attr, data)
            elif (attr not in ['title', 'changecount'] and
                not attr.startswith('server.')):
                tiddler.fields[attr] = data
    if not node.get('modified', None) and tiddler.created:
        tiddler.modified = tiddler.created
    tiddler.tags = _tag_string_to_list(node.get('tags', ''))

    return tiddler


def _tag_string_to_list(string):
    """
    Turn a string of tags in TiddlyWiki format into a list.
    """
    return string_to_tags_list(string)


def _html_decode(text):
    """
    Decode HTML entities used in TiddlyWiki content into the 'real' things.
    """
    return text.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&').replace('&quot;', '"')
