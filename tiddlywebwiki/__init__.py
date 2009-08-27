"""
A TiddlyWeb plugin providing a multi-user TiddlyWiki environment.
"""

import tiddlywebwiki.fromsvn
import tiddlywebwiki.instancer
import tiddlywebwiki.twanager
from tiddlyweb.config import merge_config
from tiddlywebwiki.config import config as twwconfig


__version__ = '0.8'


def init(config):
    merge_config(config, twwconfig)
    tiddlywebwiki.fromsvn.init(config)
    tiddlywebwiki.instancer.init(config)
    tiddlywebwiki.twanager.init(config)
    # XXX and add selector for POST a wiki
