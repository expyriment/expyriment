# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>


html_documentation:
	make --directory=documentation/sphinx html
	rm -rf documentation/html
	mv documentation/sphinx/_build/html documentation/html 

pdf_documentation:
	make --directory=documentation/sphinx pdf
	rm -rf documentation/latex
	mv -f documentation/sphinx/_build/latex documentation/latex

api_ref_html:
	make --directory=documentation/api html
	rm -rf documentation/api_ref_html
	mv -f documentation/api/_build documentation/api_ref_html

release: html_documentation api_ref_html
	python setup.py build

build:
	mkdir build

clean:
	make --directory=documentation/sphinx clean
	make --directory=documentation/api clean
	rm -rf build documentation/latex documentation/api_ref documentation/html 
