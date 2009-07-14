"""
Test twanager commands.
"""

import sys
sys.path.insert(0, '.')

import os

from shutil import rmtree

from tiddlyweb.config import config

import tiddlywebwiki.instancer as instancer
import tiddlywebwiki.twanager as twanager


instance_dir = 'test_instance'


def setup_module(module):
    instancer.init(config)
    twanager.init(config)
    try:
        rmtree(instance_dir)
    except:
        pass


class TestInstance(object):

    def teardown_method(self, module):
        os.chdir('..')
        rmtree(instance_dir)

    def test_create_tiddlywebwiki_instance(self):
        twanager.instance([instance_dir])

        contents = _get_file_contents('../%s/tiddlywebconfig.py' % instance_dir)

        assert "'system_plugins': ['tiddlywebwiki.plugin']" in contents
        assert "'twanager_plugins': ['tiddlywebwiki.plugin']" in contents

    def test_create_bag_policies(self):
        twanager.instance([instance_dir])

        policy_location = '../%s/store/bags/%%s/policy' % instance_dir

        system_policy = _get_file_contents(policy_location % "system")
        common_policy = _get_file_contents(policy_location % "common")

        assert '"read": []' in system_policy
        assert '"write": ["R:ADMIN"]' in system_policy
        assert '"create": ["R:ADMIN"]' in system_policy
        assert '"manage": ["R:ADMIN"]' in system_policy
        assert '"accept": ["R:ADMIN"]' in system_policy
        assert '"delete": ["R:ADMIN"]' in system_policy

        assert '"delete": ["R:ADMIN"]' in common_policy


def _get_file_contents(filepath):
    f = open(filepath)
    contents = f.read()
    f.close()
    return contents
