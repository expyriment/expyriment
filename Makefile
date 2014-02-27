# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: build install clean

release: build html_documentation api_ref_html pdf_documentation
	@# requires numpydoc. install: easy_install numpydoc
	make --directory=documentation/sphinx clean
	make --directory=documentation/api clean
	@echo "copy files"
	@mv build/lib* build/release
	@cp -ra documentation build/release
	@cp -ra examples build/release
	@cp -at build/release  CHANGES.md COPYING.txt README.md 
	@cp -at build/release  setup.py
	@# get version and rename and zip
	@VER=$$(awk -F' ' '{if ($$2=="Version:") print $$3}' < /tmp/expy.build.log); \
		cd build;\
		rm -rf expyriment-$$VER;\
		mv release expyriment-$$VER;\
		zip -r expyriment-$$VER.zip expyriment-$$VER;\
		tar czf expyriment-$$VER.tar.gz expyriment-$$VER;
	@find build -type f \( -name '*.swp' -o -name '*~' -o -name '*.bak' -o -name '#*#' \) -delete
	

build:
	python setup.py build | tee /tmp/expy.build.log

install:
	python setup.py install

html_documentation:
	make --directory=documentation/sphinx html
	rm -rf documentation/html
	cp -ra documentation/sphinx/_build/html documentation/html 

pdf_documentation:
	make --directory=documentation/sphinx latexpdf
	mkdir -p documentation/pdf
	cp -ra documentation/sphinx/_build/latex/Expyriment.pdf documentation/pdf

api_ref_html:
	make --directory=documentation/api html
	rm -rf documentation/api_ref_html
	cp -ra documentation/api/_build documentation/api_ref_html

clean:
	make --directory=documentation/sphinx clean
	make --directory=documentation/api clean
	rm -rf build documentation/pdf documentation/api_ref_html documentation/html 
