"""
Test twanager commands.
"""

import sys
sys.path.insert(0, '.')

from shutil import rmtree

from tiddlywebwiki.twanager import instance


def test_tiddlywebwiki_instance():

    instance_dir = "test_instance"
    instance([instance_dir])

    f = open("test_instance/tiddlywebconfig.py")
    contents = f.read()
    f.close()
    rmtree(instance_dir)

    assert "'system_plugins': ['tiddlywebwiki.plugin']" in contents
    assert "'twanager_plugins': ['tiddlywebwiki.plugin']" in contents
