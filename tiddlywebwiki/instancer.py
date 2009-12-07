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
import time

from tiddlyweb.config import config
from tiddlyweb.util import sha
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlywebwiki.importer import import_list
from tiddlywebplugins.utils import get_store


CONFIG_NAME = 'tiddlywebconfig.py'


def instance(directory, system_config=None):
    """Create a TiddlyWebWiki instance in the given directory"""
    if not directory:
        raise ValueError('You must provide the name of a directory.')
    if os.path.exists(directory):
        raise IOError('Your chosen directory already exists. Choose a different name.')

    if system_config == None:
        system_config = {}
    store = get_store(system_config)

    cfg = {
        'system_plugins': ['tiddlywebwiki', 'tiddlywebplugins.status', 'differ'],
        'twanager_plugins': ['tiddlywebwiki']
    }
    create_instance(directory, config, defaults=cfg, system_config=system_config)

    bag = Bag('system')
    bag.policy.write = ['R:ADMIN']
    bag.policy.create = ['R:ADMIN']
    bag.policy.delete = ['R:ADMIN']
    bag.policy.manage = ['R:ADMIN']
    bag.policy.accept = ['R:ADMIN']
    store.put(bag)

    bag = Bag('common')
    bag.policy.delete = ['R:ADMIN']
    bag.policy.manage = ['R:ADMIN']
    store.put(bag)

    recipe = _make_recipe('default', ['system', 'common'], store)


def create_instance(directory, cfg, defaults=None, system_config=None):
    """
    Create a TiddlyWeb instance directory.

    accepts an optional dictionary with default configuration values
    """
    os.mkdir(directory)
    os.chdir(directory)
    _generate_config(defaults)
    store = get_store(system_config)
    instance_tiddlers = cfg.get('instance_tiddlers', {})
    bag_names = [bag for bag, tiddlers in instance_tiddlers.items()]
    for bag in bag_names:
        bag = Bag(bag)
        store.put(bag)
    update_instance(system_config)


def update_instance(cfg=None):
    """
    Update a TiddlyWeb instance by reimporting instance_tiddlers.
    """
    if cfg == None:
        cfg = {}
    instance_tiddlers = cfg.get('instance_tiddlers', {})
    [import_list(bag, tiddlers, cfg) for bag, tiddlers
        in instance_tiddlers.items()]


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
    digest = sha(str(time.time()))
    digest.update(str(random.random()))
    digest.update('tiddlyweb and tiddlywiki are rad')
    return digest.hexdigest()


def _make_recipe(recipe_name, bags, store):
    """Make a recipe with recipe_name."""
    recipe = Recipe(recipe_name)
    recipe_list = [[bag, ''] for bag in bags]
    recipe.set_recipe(recipe_list)
    store.put(recipe)
