# Simple Makefile for some common tasks. This will get 
# fleshed out with time to make things easier on developer
# and tester types.
.PHONY: test dist upload

empty:
	wget http://tiddlywiki.com/empty.html -O tiddlywebwiki/empty.html
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
	scp CHANGES dist/tiddlywebwiki-*.gz cdent@peermore.com:public_html/peermore.com/tiddlyweb/dist
