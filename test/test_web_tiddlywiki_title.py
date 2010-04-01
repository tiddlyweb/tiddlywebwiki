import wsgi_intercept
import httplib2

from wsgi_intercept import httplib2_intercept

from tiddlyweb.model.tiddler import Tiddler

from fixtures import muchdata, reset_textstore, _teststore


def setup_module(module):
    from tiddlyweb.web import serve
    # we have to have a function that returns the callable,
    # Selector just _is_ the callable
    def app_fn():
        return serve.load_app()
    #wsgi_intercept.debuglevel = 1
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('our_test_domain', 8001, app_fn)

    reset_textstore()
    module.store = _teststore()
    muchdata(module.store)


def test_get_wiki():
    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/recipes/long/tiddlers.wiki',
            method='GET')

    assert response['status'] == '200'
    assert response['content-type'] == 'text/html; charset=UTF-8'
    assert '\n<title>\nTiddlyWeb Loading\n</title>\n' in content
    assert 'i am tiddler 8' in content


def test_get_wiki_with_title():
    tiddler = Tiddler('SiteTitle')
    tiddler.bag = u'bag1'
    tiddler.text = u'Wow //cow// moo'

    store.put(tiddler)

    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/recipes/long/tiddlers.wiki',
            method='GET')

    assert response['status'] == '200'
    assert '\n<title>\nWow cow moo\n</title>\n' in content
    assert 'Wow //cow// moo' in content

    tiddler = Tiddler('SiteSubtitle')
    tiddler.bag = u'bag1'
    tiddler.text = u'MooCow'
    store.put(tiddler)

    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/recipes/long/tiddlers.wiki',
            method='GET')

    assert response['status'] == '200'
    assert '<title>\nWow cow moo - MooCow\n</title>' in content
    assert 'MooCow' in content

    tiddler = Tiddler('SiteTitle')
    tiddler.bag = u'bag1'
    store.delete(tiddler)

    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/recipes/long/tiddlers.wiki',
            method='GET')

    assert response['status'] == '200'
    assert '<title>\nMooCow\n</title>' in content
    assert 'MooCow' in content

    tiddler = Tiddler('MarkupPreHead', 'bag1')
    tiddler.text = 'UNIQUE9578'
    store.put(tiddler)

    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/recipes/long/tiddlers.wiki',
            method='GET')

    assert response['status'] == '200'
    assert '<!--PRE-HEAD-START-->\nUNIQUE9578\n<!--PRE-HEAD-END-->' in content

    tiddler = Tiddler('WindowTitle')
    tiddler.bag = u'bag1'
    tiddler.text = u'A window title'

    store.put(tiddler)

    http = httplib2.Http()
    response, content = http.request('http://our_test_domain:8001/recipes/long/tiddlers.wiki',
            method='GET')
    assert response['status'] == '200'
    # WindowTitle overrides the SiteTitle created up the stack
    assert '<title>\nA window title\n</title>' in content
