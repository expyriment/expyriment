# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: install clean build testpypi publish

html_documentation: documentation/html
pdf_documentation: documentation/Expyriment.pdf


release:
	flit build

testpypi:
	flit --repository testpypi publish

publish:
	flit publish

documentation/html:
	make --directory=documentation/sphinx rst html
	mv documentation/sphinx/_build/html documentation/html
# FIXME SITEMAP DOES NOT WORK
#make --directory=documentation/sphinx sitemap
#mv documentation/sphinx/sitemap.yml documentation/html/

documentation/Expyriment.pdf:
	make --directory=documentation/sphinx rst latexpdf
	mv documentation/sphinx/_build/latex/Expyriment.pdf documentation/


clean:
	@make --directory=documentation/sphinx clean
	@rm -rf build \
			dist \
			expyriment.egg-info \
			documentation/Expyriment.pdf\
			documentation/api_ref_html\
			documentation/html
	@find . -name '*.py[co]' \
		 -o -iname '#*#' | xargs -L 10 rm -f
