"""
Test twanager commands.
"""

import os

import tiddlywebwiki

import tiddlywebwiki.instance as instance_module

from shutil import rmtree

from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.bag import Bag

from tiddlywebplugins.instancer.util import spawn


instance_dir = 'test_instance'


def setup_module(module):
    tiddlywebwiki.init(config)
    tiddlywebwiki.manage.init(config)
    try:
        rmtree(instance_dir)
    except:
        pass

    instance_tiddlers = config['instance_tiddlers']
    for bag, uris in instance_tiddlers.items():
        # ensure that HTTP URLs are not used -- XXX: this is a temporary workaround until we have proper tests
        for uri in uris:
            if uri.startswith('http'):
                raise ValueError('must not use HTTP URLs; use cacher for local copies')
        # adjust relative paths to account for instancer's chdir operation -- XXX: obsolete?
        instance_tiddlers[bag] = [
            uri.replace('file:./', 'file:../') for uri in uris
            ]


class TestInstance(object):

    def setup_method(self, module):
        env = { 'tiddlyweb.config': config }
        self.store = Store(config['server_store'][0], config['server_store'][1], environ=env)

    def teardown_method(self, module):
        os.chdir('..')
        rmtree(instance_dir)

    def test_create_tiddlywebwiki_instance(self):
        spawn(instance_dir, config, instance_module)

        contents = _get_file_contents('../%s/tiddlywebconfig.py' % instance_dir)

        assert "'system_plugins': ['tiddlywebwiki']" in contents
        assert "'twanager_plugins': ['tiddlywebwiki']" in contents

    def test_create_bag_policies(self):
        spawn(instance_dir, config, instance_module)

        bag = Bag('system')
        system_policy = self.store.get(bag).policy
        bag = Bag('common')
        common_policy = self.store.get(bag).policy

        assert system_policy.read == []
        assert system_policy.write == ['R:ADMIN']
        assert system_policy.create == ['R:ADMIN']
        assert system_policy.manage == ['R:ADMIN']
        assert system_policy.accept == ['R:ADMIN']
        assert system_policy.delete == ['R:ADMIN']

        assert common_policy.read == []
        assert common_policy.write == []
        assert common_policy.create == []
        assert common_policy.manage == ['R:ADMIN']
        assert common_policy.accept == []
        assert common_policy.delete == []


def _get_file_contents(filepath):
    f = open(filepath)
    contents = f.read()
    f.close()
    return contents
