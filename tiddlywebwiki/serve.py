"""
Replace the default (slow) wsgiref server with
a faster (because of threads) web server. Only
used if the instanced is started with "twanager
server".

See the "wsgi_server" entry in tidddlyweb.config.
"""

import logging
import sys

from tiddlyweb.util import std_error_message
from tiddlyweb.web.serve import load_app

LOGGER = logging.getLogger(__name__)


def start_server(config):
    from cherrypy.wsgiserver import CherryPyWSGIServer
    hostname = config['server_host']['host']
    port = int(config['server_host']['port'])
    scheme = config['server_host']['scheme']
    app = load_app()
    server = CherryPyWSGIServer((hostname, port), app)
    try:
        LOGGER.debug('starting CherryPy at %s://%s:%s',
                scheme, hostname, port)
        std_error_message("Starting CherryPy at %s://%s:%s"
                % (scheme, hostname, port))
        server.start()
    except KeyboardInterrupt:
        server.stop()
        sys.exit(0)
