"""
A built-in twanager plugin for setting up a new instance
of TiddlyWeb, to lighten the load on getting started.

Example:

    twanager instance foo

This will create a foo directory containing:

    * empty tiddlywebconfig.py
    * store directory with a system bag containing
      the important plugins (assuming text store is
      in default config.py)
"""

import os
import random
import sha
import time

from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.store import Store
from tiddlyweb.manage import make_command
from tiddlywebwiki.fromsvn import import_list


CONFIG_NAME = 'tiddlywebconfig.py'


def _generate_secret():
    """
    Create a somewhat random secret to be used
    for message authentication.
    """
    digest = sha.sha(str(time.time()))
    digest.update(str(random.random()))
    digest.update('tiddlyweb and tiddlywiki are rad')
    return digest.hexdigest()


EMPTY_CONFIG = """# A basic config, make your own changes here.
# Run 'pydoc tiddlyweb.config' for information on changing the defaults.
config = {
    'secret': '%s',
}
""" % _generate_secret()


@make_command()
def instance(args):
    """Create a TiddlyWeb instance using instance_tiddlers in the given directory: <dir>"""
    directory = args[0]
    if not directory:
        raise ValueError('You must provide the name of a directory.')
    if os.path.exists(directory):
        raise IOError('Your chosen directory already exists. Choose a different name.')
    os.mkdir(directory)
    os.chdir(directory)
    _empty_config()
    bag_names = [bag for bag, tiddlers in config['instance_tiddlers']]
    for bag in bag_names:
        bag = Bag(bag)
        _store_bag(bag)
    update(None)


@make_command()
def update(args):
    """Update all instance_tiddlers in the current instance."""
    [import_list(bag, tiddlers) for bag, tiddlers in
            config['instance_tiddlers']]


def _empty_config():
    """Write an empty tiddlywebconfig.py to the CWD."""
    cfg = open(CONFIG_NAME, 'w')
    cfg.write(EMPTY_CONFIG)
    cfg.close()


def _make_recipe(recipe_name, bags):
    """Make a recipe with recipe_name."""
    recipe = Recipe(recipe_name)
    recipe_list = [[bag, ''] for bag in bags]
    recipe.set_recipe(recipe_list)
    store = Store(config['server_store'][0], environ={'tiddlyweb.config': config})
    store.put(recipe)


def _store_bag(bag): # XXX: too simple to warrant a dedicated function!?
    """Add a Bag instance to the store."""
    store = Store(config['server_store'][0], environ={'tiddlyweb.config': config})
    store.put(bag)


def init(config_in):
    """Initialize the plugin with config."""
    global config
    config = config_in
