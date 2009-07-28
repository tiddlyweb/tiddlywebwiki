"""
A plugin to hold the TiddlyWebWiki code together.
"""

import tiddlywebwiki.fromsvn
import tiddlywebwiki.instancer
import tiddlywebwiki.twanager
from tiddlyweb.config import merge_config
from tiddlywebwiki.config import config as twwconfig


def init(config):
    merge_config(config, twwconfig)
    # XXX and add selector for POST a wiki
