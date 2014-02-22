# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>


html_documentation: build
	make --directory=documentation/sphinx html
	ln -fs ../documentation/sphinx/build/html build/html

pdf_documentation: build
	make --directory=documentation/sphinx pdf
	ln -fs ../documentation/sphinx/build/latex build/latex

old_html_api: build
	make --directory=documentation/api html
	mv documentation/api/_build build/old_html_api

install:
	@echo "TODO"

release: build
	python setup.py build
	@echo "TODO"

build:
	mkdir build

clean:
	make --directory=documentation/sphinx clean
	make --directory=documentation/api clean
	rm -rf build
