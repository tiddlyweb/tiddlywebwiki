"""
Test instance creation.
"""

import os

from shutil import rmtree

import tiddlywebwiki.instancer as instancer

from tiddlyweb.config import config as system_config


instance_dir = 'test_instance'
config = {
    'instance_tiddlers': {}
}


def setup_module(module):
    try:
        rmtree(instance_dir)
    except:
        pass


class TestCreateInstance(object):

    def teardown_method(self, module):
        os.chdir('..')
        rmtree(instance_dir)

    def test_create_default(self):
        instancer.create_instance(instance_dir, config, system_config=system_config)
        contents = _get_file_contents('../%s/tiddlywebconfig.py' % instance_dir)

        assert 'config = {\n' in contents
        assert "'secret': '" in contents
        assert '\n}' in contents

    def test_create_custom(self):
        defaults = {
            'foo': 'lorem',
            'bar': 'ipsum'
        }
        instancer.create_instance(instance_dir, config, defaults=defaults,
                system_config=system_config)
        contents = _get_file_contents('../%s/tiddlywebconfig.py' % instance_dir)

        assert 'config = {\n' in contents
        assert "'foo': 'lorem'" in contents
        assert "'bar': 'ipsum'" in contents
        assert '\n}' in contents


def _get_file_contents(filepath):
    f = open(filepath)
    contents = f.read()
    f.close()
    return contents
