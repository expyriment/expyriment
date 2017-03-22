# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: install clean

html_documentation: documentation/html
pdf_documentation: documentation/Expyriment.pdf
api_ref_html: documentation/api_ref_html
release: wheel tarball 
wheel: dist build/wheel_version

tarball: dist build/wheel_version
	@VER=$$(cat build/wheel_version);\
		DIR=python-expyriment-$$VER;\
		TAR=python-expyriment_$$VER.orig.tar.gz;\
		mkdir -p build/$$DIR ;\
		mkdir -p build/tmp ;\
		unzip dist/* -d build/tmp ;\
		mv build/tmp/expyriment build/$$DIR ;\
		rm -rf build/tmp ;\
		rm build/$$DIR/expyriment/_fonts -rf ;\
		cp -ra documentation build/$$DIR ;\
		rm build/$$DIR/documentation/sphinx/_build -r ;\
		cp -at build/$$DIR  CHANGES.md COPYING.txt README.md ;\
		cp -at build/$$DIR setup.py ;\
		find build/$$DIR -type f -name '*.swp' -o -name '*~' -o -name '*.bak'\
		-o -name '*.py[co]' -o -iname '#*#' | xargs -L 5 rm -f ;\
		cd build ;\
		rm -f $$TAR;\
		tar cfz $$TAR $$DIR;\
		rm -rf $$DIR;\
		mv $$TAR ../dist/

dist:
	mkdir -p build
	python setup.py bdist_wheel --universal | tee build/wheel.log

build/wheel_version: dist 
	@grep "Expyriment Version:" build/wheel.log | sed  \
				-e 's/.*\(\[.\+\]\).*/\1/g'  \
				-e "s/\]//" -e "s/\[//" > build/wheel_version 

install:
	python setup.py install

documentation/html:
	make --directory=documentation/sphinx rst html sitemap
	mv documentation/sphinx/_build/html documentation/html
	mv documentation/sphinx/sitemap.yml documentation/html/

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
