# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>


html_documentation:
	make --directory=documentation/sphinx html
	mkdir -p _build
	ln -fs ../documentation/sphinx/_build/html _build/html

pdf_documentation:
	make --directory=documentation/sphinx pdf
	mkdir -p _build
	ln -fs ../documentation/sphinx/_build/latex _build/latex

install:
	@echo "TODO"

release:
	@echo "TODO"

clean:
	make --directory=documentation/sphinx clean
	rm -rf _build
