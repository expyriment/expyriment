# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: install clean build testpypi publish

build:
	flit build

install:
	flit install

testpypi:
	flit --repository testpypi publish

publish:
	flit publish

clean:
	@rm -rf build \
			dist \
			expyriment.egg-info
	@find . -name '*.py[co]' \
		 -o -iname '#*#' | xargs -L 10 rm -f
