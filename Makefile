# Simple Makefile for some common tasks. This will get 
# fleshed out with time to make things easier on developer
# and tester types.
.PHONY: test dist upload

all:
	@echo "No target"

empty:
	wget http://tiddlywiki.com/empty.html -O tiddlywebwiki/empty.html

status_plugin:
	wget http://github.com/tiddlyweb/tiddlyweb-plugins/raw/master/status/status.py -O status.py

wikklytextrender_plugin:
	wget http://github.com/tiddlyweb/tiddlyweb-plugins/raw/master/wikklytextrender/wikklytextrender.py -O wikklytextrender.py

twebplugins: status_plugin wikklytextrender_plugin

remotes: empty twebplugins

clean:
	rm -r dist || true

test: 
	py.test -x test

dist: test
	python setup.py sdist

upload: clean test pypi peermore

pypi:
	python setup.py sdist upload

peermore:
	scp dist/tiddlywebwiki-*.gz cdent@peermore.com:public_html/peermore.com/tiddlyweb/dist
	scp CHANGES cdent@peermore.com:public_html/peermore.com/tiddlyweb/dist/CHANGES.tiddlywebwiki
