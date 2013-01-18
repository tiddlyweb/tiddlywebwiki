"""
Serialize into a fullblown tiddlywiki wiki.

The generated wiki comes from config['base_tiddlywiki'] injected
with a tiddlywiki div representation of each included tiddler.

For those tiddlers which are considered binary (e.g. contain an
image, an application, etc) the contents of tiddler.text is sent
as the base64 encoding of that text. Client side plugins can 
turn that into a data: style URI and use the content.

If config['tiddlywebwiki.binary_limit'] is set to some integer
value that value sets a limit above which the base64 content is
_not_ sent. Instead a link is made back to the server. If 
tiddler.type matches 'image/' then the link is an <img> tag.
Otherwise an anchor.
"""

from base64 import b64encode

from tiddlyweb.serializations import SerializationInterface
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.util import binary_tiddler
from tiddlyweb.web.util import (server_base_url, tiddler_url,
        encode_name, html_encode, escape_attribute_value)
from tiddlyweb.web.util import tiddler_etag
from tiddlyweb.store import StoreError


SPLITTER = '</div>\n<!--POST-STOREAREA-->\n'

MARKUPS = {
    'MarkupPreHead': 'PRE-HEAD',
    'MarkupPostHead': 'POST-HEAD',
    'MarkupPreBody': 'PRE-BODY',
    'MarkupPostBody': 'POST-SCRIPT',
    }

WIKI = ''


class Serialization(SerializationInterface):
    """
    Serialize entities and collections to and from
    TiddlyWiki representations. This is primarily
    used to create TiddlyWikis from bags, recipes
    and tiddlers. It can also be used to import
    TiddlyWikis into the system.
    """

    def list_tiddlers(self, bag):
        """
        Take the tiddlers from the given bag and inject
        them into a TiddlyWiki.
        """
        try:
            return self._put_tiddlers_in_tiddlywiki(bag.list_tiddlers())
        except AttributeError:
            return self._put_tiddlers_in_tiddlywiki(bag)

    def tiddler_as(self, tiddler):
        """
        Take the single tiddler provided and inject it into
        a TiddlyWiki.
        """
        return ''.join(self._put_tiddlers_in_tiddlywiki(
            [tiddler], title=tiddler.title))

    def _no_script(self, url):
        """
        Inject noscript content into the created wiki to provide
        a link to indexable content.

        Often overridden.
        """
        if url:
            return """
<div id="javascriptWarning">
This page requires JavaScript to function properly.<br /><br />
If you do not use JavaScript you may still <a href="%s">browse
the content of this wiki</a>.
</div>
""" % url
        else:
            return ''

    def _put_tiddlers_in_tiddlywiki(self, tiddlers, title='TiddlyWeb Loading'):
        """
        Take the provided tiddlers and inject them into the base_tiddlywiki,
        adjusting content for title, subtite, and the various pre and post
        head sections of the file.
        """

        (browsable_url, kept_tiddlers, title,
                found_markup_tiddlers) = self._create_tiddlers(title, tiddlers)

        # load the wiki
        wiki = self._get_wiki()
        # put the title in place
        wiki = self._inject_title(wiki, title)

        wiki = self._replace_chunk(wiki, '\n<noscript>\n', '\n</noscript>\n',
                self._no_script(browsable_url))

        # replace the markup bits
        for tiddler_title in found_markup_tiddlers:
            start = '\n<!--%s-START-->\n' % MARKUPS[tiddler_title]
            finish = '\n<!--%s-END-->\n' % MARKUPS[tiddler_title]
            wiki = self._replace_chunk(wiki, start, finish,
                    found_markup_tiddlers[tiddler_title])

        # split the wiki into the before store and after store
        # sections, put our content in the middle
        tiddlystart, tiddlyfinish = wiki.split(SPLITTER, 2)
        yield tiddlystart
        for tiddler in kept_tiddlers:
            yield self._tiddler_as_div(tiddler)
        yield SPLITTER
        yield tiddlyfinish
        return

    def _create_tiddlers(self, title, tiddlers):
        """
        Figure out the content to be pushed into the
        wiki and calculate the title.
        """
        kept_tiddlers = []
        window_title = None
        candidate_title = None
        candidate_subtitle = None
        markup_tiddlers = MARKUPS.keys()
        found_markup_tiddlers = {}
        for tiddler in tiddlers:
            kept_tiddlers.append(tiddler)
            tiddler_title = tiddler.title
            if tiddler_title == 'WindowTitle':
                window_title = tiddler.text
            if tiddler_title == 'SiteTitle':
                candidate_title = tiddler.text
            if tiddler_title == 'SiteSubtitle':
                candidate_subtitle = tiddler.text
            if tiddler_title in markup_tiddlers:
                found_markup_tiddlers[tiddler_title] = tiddler.text

        if len(kept_tiddlers) == 1:
            default_tiddler = Tiddler('DefaultTiddlers', '_virtual')
            default_tiddler.text = '[[' + tiddler.title + ']]'
            kept_tiddlers.append(default_tiddler)

        browsable_url = None
        try:
            if tiddler.recipe:
                workspace = '/recipes/%s/tiddlers' % encode_name(tiddler.recipe)
            else:
                workspace = '/bags/%s/tiddlers' % encode_name(tiddler.bag)
            browsable_url = server_base_url(self.environ) + workspace
        except UnboundLocalError:
            pass # tiddler is not set because tiddlers was empty

        # Turn the title into HTML and then turn it into
        # plain text so it is of a form satisfactory to <title>
        title = self._determine_title(title, window_title, candidate_title,
                candidate_subtitle)

        return browsable_url, kept_tiddlers, title, found_markup_tiddlers

    def _determine_title(self, title, window_title, candidate_title, candidate_subtitle):
        """
        Create a title for the wiki file from various
        optional inputs.
        """
        if window_title:
            return window_title
        if candidate_title and candidate_subtitle:
            return '%s - %s' % (candidate_title, candidate_subtitle)
        if candidate_title:
            return candidate_title
        if candidate_subtitle:
            return candidate_subtitle
        return title

    def _inject_title(self, wiki, title):
        """
        Replace the title in the base_tiddlywiki
        with our title.
        """
        return self._replace_chunk(wiki, '\n<title> ', ' </title>\n', title)

    def _replace_chunk(self, wiki, start, finish, replace):
        """
        Find the index of start and finish in the string, and
        replace the part in between with replace.
        """
        try:
            sindex = wiki.index(start)
            findex = wiki.index(finish) + len(finish)
            return wiki[0:sindex] + start + replace + finish + wiki[findex:]
        except ValueError:
            return wiki

    def _get_wiki(self):
        """
        Read base_tiddlywiki from its location.
        """
        global WIKI
        if WIKI:
            return WIKI
        base_tiddlywiki = open(
            self.environ['tiddlyweb.config']['base_tiddlywiki'])
        wiki = base_tiddlywiki.read()
        base_tiddlywiki.close()
        wiki = unicode(wiki, 'utf-8')
        WIKI = wiki
        return WIKI

    def _tiddler_as_div(self, tiddler):
        """
        Read in the tiddler from a div.
        """
        recipe_name = ''
        if tiddler.recipe:
            recipe_name = tiddler.recipe
        try:
            host = server_base_url(self.environ)
        except KeyError:
            host = ''
        host = '%s' % host

        if binary_tiddler(tiddler):
            tiddler_output = self._binary_tiddler(tiddler)
        else:
            tiddler_output = tiddler.text

        if tiddler.type == 'None' or not tiddler.type:
            tiddler.type = ''

        return ('<div title="%s" server.title="%s" server.page.revision="%s" '
                'server.etag="%s" '
                'modifier="%s" creator="%s" server.workspace="bags/%s" '
                'server.type="tiddlyweb" server.host="%s" '
                'server.recipe="%s" server.bag="%s" server.permissions="%s" '
                'server.content-type="%s" '
                'modified="%s" created="%s" tags="%s" %s>\n'
                '<pre>%s</pre>\n</div>\n' %
                    (escape_attribute_value(tiddler.title),
                        escape_attribute_value(tiddler.title),
                        tiddler.revision,
                        escape_attribute_value(tiddler_etag(
                            self.environ, tiddler)),
                        escape_attribute_value(tiddler.modifier),
                        escape_attribute_value(tiddler.creator),
                        escape_attribute_value(tiddler.bag),
                        host,
                        escape_attribute_value(recipe_name),
                        escape_attribute_value(tiddler.bag),
                        self._tiddler_permissions(tiddler),
                        tiddler.type,
                        tiddler.modified,
                        tiddler.created,
                        escape_attribute_value(self.tags_as(tiddler.tags)),
                        self._tiddler_fields(tiddler.fields),
                        html_encode(tiddler_output)))

    def _tiddler_permissions(self, tiddler):
        """
        Make a list of the permissions the current user has
        on this tiddler.
        """

        def _read_bag_perms(environ, tiddler):
            """
            Get the permissions of the bag this tiddler is in.
            """
            perms = []
            if 'tiddlyweb.usersign' in environ:
                store = tiddler.store
                if store:
                    try:
                        bag = Bag(tiddler.bag)
                        bag = store.get(bag)
                        perms = bag.policy.user_perms(
                                environ['tiddlyweb.usersign'])
                    except StoreError:
                        pass
            return perms

        perms = []
        bag_name = tiddler.bag
        if hasattr(self, 'bag_perms_cache'):
            if bag_name in self.bag_perms_cache:
                perms = self.bag_perms_cache[bag_name]
            else:
                perms = _read_bag_perms(self.environ, tiddler)
        else:
            self.bag_perms_cache = {}
            perms = _read_bag_perms(self.environ, tiddler)
        self.bag_perms_cache[bag_name] = perms
        return ', '.join(perms)

    def _binary_tiddler(self, tiddler):
        """
        Make the content for a tiddler that has non-wikitext content.
        """
        limit = self.environ['tiddlyweb.config'].get(
                'tiddlywebwiki.binary_limit', 0)
        if limit and len(tiddler.text) > limit:
            if tiddler.type.startswith('image/'):
                return ('\n<html><img src="%s" /></html>\n' %
                        tiddler_url(self.environ, tiddler))
            else:
                return ('\n<html><a href="%s">%s</a></html>\n' %
                        (tiddler_url(self.environ, tiddler), tiddler.title))
        else:
            return b64encode(tiddler.text)

    def _tiddler_fields(self, fields):
        """
        Turn tiddler fields into a string suitable for
        a div attribute.
        """
        output = []
        for key, val in fields.items():
            output.append('%s="%s"' % (key, escape_attribute_value(val)))
        return ' '.join(output)
