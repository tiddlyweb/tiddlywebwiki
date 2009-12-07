"""
Test twanager commands.
"""

import os

import tiddlywebwiki as tww

from shutil import rmtree

from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.bag import Bag


instance_dir = 'test_instance'


def setup_module(module):
    tww.init(config)
    tww.manage.init(config)
    try:
        rmtree(instance_dir)
    except:
        pass

    # adjust relative paths to account for instancer's chdir operation -- XXX: obsolete?
    instance_tiddlers = tww.manage.config['instance_tiddlers']
    for bag, uris in instance_tiddlers.items():
        instance_tiddlers[bag] = [
            uri.replace('file:./', 'file:../') for uri in uris
            ]


class TestInstance(object):

    def setup_method(self, module):
        env = { 'tiddlyweb.config': config }
        self.store = Store(config['server_store'][0], environ=env)

    def teardown_method(self, module):
        os.chdir('..')
        rmtree(instance_dir)

    def test_create_tiddlywebwiki_instance(self):
        tww.instancer.instance(instance_dir, system_config=config)

        contents = _get_file_contents('../%s/tiddlywebconfig.py' % instance_dir)

        assert "'system_plugins': ['tiddlywebwiki', 'tiddlywebplugins.status', 'differ']" in contents
        assert "'twanager_plugins': ['tiddlywebwiki']" in contents

    def test_create_bag_policies(self):
        tww.instancer.instance(instance_dir, config)

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
        assert common_policy.delete == ['R:ADMIN']


def _get_file_contents(filepath):
    f = open(filepath)
    contents = f.read()
    f.close()
    return contents
