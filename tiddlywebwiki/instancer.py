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


EMPTY_CONFIG = {
    'secret': '%s' % _generate_secret()
}


@make_command()
def instance(args, config=None): # XXX: accepting additional argument hacky?
    """Create a TiddlyWeb instance using instance_tiddlers in the given directory: <dir>"""
    directory = args[0]
    if not directory:
        raise ValueError('You must provide the name of a directory.')
    if os.path.exists(directory):
        raise IOError('Your chosen directory already exists. Choose a different name.')
    os.mkdir(directory)
    os.chdir(directory)
    _generate_config(config)
    bag_names = [bag for bag, tiddlers in config['instance_tiddlers']] # XXX: KeyError on instance_tiddlers
    for bag in bag_names:
        bag = Bag(bag)
        _store_bag(bag)
    update(None)


@make_command()
def update(args):
    """Update all instance_tiddlers in the current instance."""
    [import_list(bag, tiddlers) for bag, tiddlers in
            config['instance_tiddlers']]


def _generate_config(config=None):
    """
    Write a default tiddlywebconfig.py to the CWD.

    accepts an optional dictionary with configuration values
    defaults to global EMPTY_CONFIG
    """
    config = config or EMPTY_CONFIG # TODO: merge so secret is retained
    lines = ["    '%s': '%s'" % (k, v) for k, v in config.items()]
    config = 'config = {\n%s\n}\n' % ',\n'.join(lines) # XXX: use pprint?
    intro = '%s\n%s' % ('# A basic configuration.',
        "# Run 'pydoc tiddlyweb.config' for details on configuration items.")
    cfg = open(CONFIG_NAME, 'w')
    cfg.write('%s\n%s' % (intro, config))
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
