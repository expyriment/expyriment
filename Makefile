# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: install clean

html_documentation: documentation/html
pdf_documentation: documentation/Expyriment.pdf
api_ref_html: documentation/api_ref_html
build: build/release
wheel: dist build/wheel_version

tarball: dist build/wheel_version
	unzip dist/* -d build ;\
	VER=$$(cat build/wheel_version);\
	read -p "Tarball version suffix: " VERSION_SUFFIX;\
	DIR=python-expyriment-$$VER$$VERSION_SUFFIX;\
	TAR=python-expyriment_$$VER$$VERSION_SUFFIX.orig.tar.gz;\
	mkdir -p build/$$DIR ;\
	mv build/expyriment build/$$DIR ;\
	rm build/$$DIR/expyriment/_fonts -rf ;\
	cp -ra documentation build/$$DIR ;\
	cp -ra examples build/$$DIR ;\
	cp -at build/$$DIR  CHANGES.md COPYING.txt README.md ;\
	cp -at build/$$DIR setup.py ;\
	find build/$$DIR -type f -name '*.swp' -o -name '*~' -o -name '*.bak'\
	-o -name '*.py[co]' -o -iname '#*#' | xargs -L 5 rm -f ;\
	cd build ;\
	tar cfz $$TAR $$DIR;\
	rm -rf $$DIR;\
	sha1sum $$TAR

dist:
	mkdir -p build
	python setup.py bdist_wheel | tee build/wheel.log

build/wheel_version: dist 
	@grep "Expyriment Version:" build/wheel.log | sed  \
				-e 's/.*\(\[.\+\]\).*/\1/g'  \
				-e "s/\]//" -e "s/\[//" > build/wheel_version 

install:
	python setup.py install

documentation/html:
	make --directory=documentation/sphinx rst html
	mv documentation/sphinx/_build/html documentation/html

documentation/Expyriment.pdf:
	make --directory=documentation/sphinx rst latexpdf
	mv documentation/sphinx/_build/latex/Expyriment.pdf documentation/

documentation/api_ref_html:
	make --directory=documentation/api html
	mv documentation/api/_build documentation/api_ref_html

clean:
	@make --directory=documentation/sphinx clean
	@make --directory=documentation/api clean
	@rm -rf build \
			dist \
			expyriment.egg-info \
			documentation/Expyriment.pdf\
			documentation/api_ref_html\
			documentation/html
	@find . -name '*.py[co]' \
		 -o -iname '#*#' | xargs -L 10 rm -f
