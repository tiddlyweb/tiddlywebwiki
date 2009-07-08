"""
A plugin to hold the TiddlyWebWiki code together.
"""

import tiddlywebwiki.fromsvn
import tiddlywebwiki.instancer
import tiddlywebwiki.twanager
from tiddlywebwiki.config import config as twwconfig


def init(config):
    for key in twwconfig:
        try:
            # If this config item is a dict, update to
            # update it
            twwconfig[key].keys()
            try:
                config[key].update(twwconfig[key])
            except KeyError:
                config[key] = twwconfig[key]
        except AttributeError:
            config[key] = twwconfig[key]
    tiddlywebwiki.fromsvn.init(config)
    tiddlywebwiki.instancer.init(config)
    tiddlywebwiki.twanager.init(config)
    # XXX and add selector for POST a wiki
