
import wsgi_intercept
import httplib2

from wsgi_intercept import httplib2_intercept
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.config import config

from .fixtures import _teststore

def app_fn():
    from tiddlyweb.web import serve
    return serve.load_app()

def setup_module(module):

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('0.0.0.0', 8080, app_fn)

    store = _teststore()
    store.put(Bag('bagone'))
    recipe = Recipe('recipeone')
    recipe.set_recipe([('bagone', '')])
    store.put(recipe)
    tiddler = Tiddler('tiddlerone', 'bagone')
    tiddler.text = '!Oh Hai!'
    store.put(tiddler)
    module.http = httplib2.Http()


def test_get_wiki():
    response, content = http.request(
            'http://0.0.0.0:8080/recipes/recipeone/tiddlers.wiki',
            method='GET')

    assert response['status'] == '200'
    assert '!Oh Hai!' in content


def test_get_friendlywiki():
    response, content = http.request(
            'http://0.0.0.0:8080/recipeone',
            method='GET')

    assert response['status'] == '200'
    assert '!Oh Hai!' in content
