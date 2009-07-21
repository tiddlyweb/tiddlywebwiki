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


def init(config_in):
    """Initialize the plugin with config."""
    global config
    config = config_in


@make_command()
def instance(args):
    """Create a TiddlyWeb instance using instance_tiddlers in the given directory: <dir>"""
    directory = args[0]
    if not directory:
        raise ValueError('You must provide the name of a directory.')
    if os.path.exists(directory):
        raise IOError('Your chosen directory already exists. Choose a different name.')
    create_instance(directory)


@make_command()
def update(args):
    """Update all instance_tiddlers in the current instance."""
    update_instance(config)


def create_instance(directory, cfg, defaults=None):
    """
    Create a TiddlyWeb instance directory.

    accepts an optional dictionary with default configuration values
    """
    os.mkdir(directory)
    os.chdir(directory)
    _generate_config(defaults)
    bag_names = [bag for bag, tiddlers in cfg['instance_tiddlers']]
    for bag in bag_names:
        bag = Bag(bag)
        _store_bag(bag)
    update(None)


def update_instance(cfg):
    """
    Update a TiddlyWeb instance by reimporting instance_tiddlers.
    """
    [import_list(bag, tiddlers) for bag, tiddlers in cfg['instance_tiddlers']]


def _generate_config(defaults=None):
    """
    Write a default tiddlywebconfig.py to the CWD.

    accepts an optional dictionary with configuration values
    """
    intro = '%s\n%s' % ('# A basic configuration.',
        "# Run 'pydoc tiddlyweb.config' for details on configuration items.")
    cfg = {
        'secret': _generate_secret()
    }
    cfg.update(defaults or {})

    config_string = 'config = %s\n' % _pretty_print(cfg)
    cfg = open(CONFIG_NAME, 'w')
    cfg.write('%s\n%s' % (intro, config_string))
    cfg.close()


def _pretty_print(dic): # TODO: use pprint?
    """
    generate an indented string representation of a dictionary
    """
    def escape_strings(value):
        if hasattr(value, "join"): # XXX: checking for join method hacky!?
            return "'%s'" % value
        else:
            return value
    lines = ["    '%s': %s" % (k, escape_strings(v)) for k, v in dic.items()] # TODO: use double quotes (for consistency with JSON in policy files)
    return '{\n%s\n}' % ',\n'.join(lines)


def _generate_secret():
    """
    Create a pseudo-random secret to be used for message authentication.
    """
    digest = sha.sha(str(time.time()))
    digest.update(str(random.random()))
    digest.update('tiddlyweb and tiddlywiki are rad')
    return digest.hexdigest()


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
