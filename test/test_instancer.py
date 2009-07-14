"""
Test instance creation.
"""

import sys
sys.path.insert(0, '.')

from shutil import rmtree

import tiddlywebwiki.instancer as instancer


def test_create_instance():

    instancer.config = {
        'instance_tiddlers': []
    }
    instance_dir = 'test_instance'
    instancer.create_instance(instance_dir)

    f = open('../%s/tiddlywebconfig.py' % instance_dir)
    contents = f.read()
    f.close()
    rmtree('../%s' % instance_dir)

    assert 'config = {\n' in contents
    assert "'secret': '" in contents
    assert '\n}' in contents

def test_create_custom_instance():

    instancer.config = {
        'instance_tiddlers': []
    }
    instance_dir = 'test_instance'
    defaults = {
        'foo': 'lorem',
        'bar': 'ipsum'
    }
    instancer.create_instance(instance_dir)

    f = open('../%s/tiddlywebconfig.py' % instance_dir)
    contents = f.read()
    f.close()
    rmtree('../%s' % instance_dir)

    assert 'config = {\n' in contents
    assert "'secret': '" in contents
    assert '\n}' in contents
