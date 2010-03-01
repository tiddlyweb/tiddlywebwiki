# Simple Makefile for some common tasks. This will get
# fleshed out with time to make things easier on developer
# and tester types.
.PHONY: test dist upload

all:
	@echo "No target"

tiddlywiki:
	mkdir tiddlywebwiki/resources || true
	wget http://tiddlywiki.com/empty.html -O tiddlywebwiki/resources/empty.html

remotes: tiddlywiki
	./cacher

clean:
	rm -r dist || true
	rm -r build || true
	rm -r tiddlywebwiki.egg-info || true
	rm *.bundle || true
	rm -r tiddlywebwiki/resources || true
	rm -r store tiddlyweb.log || true

test: remotes
	py.test -x test

dist: test
	python setup.py sdist

release: clean remotes test pypi peermore

pypi:
	python setup.py sdist upload

peermore:
	scp -P 8022 dist/tiddlywebwiki-*.gz cdent@tiddlyweb.peermore.com:public_html/tiddlyweb.peermore.com/dist
	scp -P 8022 CHANGES cdent@tiddlyweb.peermore.com:public_html/tiddlyweb.peermore.com/dist/CHANGES.tiddlywebwiki

makebundle: clean dist
	pip bundle tiddlywebwiki-`python setup.py --version`.bundle tiddlywebwiki

uploadbundle:
	scp -P 8022 *.bundle cdent@heavy.peermore.com:public_html/tiddlyweb.peermore.com/dist

bundle: clean dist makebundle uploadbundle
