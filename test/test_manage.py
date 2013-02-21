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

from tiddlywebplugins.imaker import spawn


instance_dir = 'test_instance'


def setup_module(module):
    tiddlywebwiki.init(config)
    try:
        rmtree(instance_dir)
    except:
        pass


class TestInstance(object):

    def setup_method(self, module):
        try:
            rmtree(instance_dir)
        except:
            pass
        self.env = {'tiddlyweb.config': config}

    def test_create_tiddlywebwiki_instance(self):
        spawn(instance_dir, config, instance_module)

        contents = _get_file_contents('%s/tiddlywebconfig.py'
                % instance_dir)

        assert "'system_plugins': ['tiddlywebwiki']" in contents
        assert "'twanager_plugins': ['tiddlywebwiki']" in contents

    def test_create_bag_policies(self):
        spawn(instance_dir, config, instance_module)
        os.chdir(instance_dir)
        store = Store(config['server_store'][0],
                config['server_store'][1], environ=self.env)

        bag = Bag('system')
        system_policy = store.get(bag).policy
        bag = Bag('common')
        common_policy = store.get(bag).policy

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
        os.chdir('..')


def _get_file_contents(filepath):
    f = open(filepath)
    contents = f.read()
    f.close()
    return contents
