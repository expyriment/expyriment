# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: install clean

html_documentation: documentation/html
pdf_documentation: documentation/Expyriment.pdf
api_ref_html: documentation/api_ref_html
release: wheel sdist 
wheel: dist build/wheel_version

tarball: dist build/wheel_version
	@VER=$$(cat build/wheel_version);\
		DIR=expyriment-$$VER;\
		TAR=expyriment_$$VER.tar.gz;\
		ZIP=expyriment_$$VER.zip;\
		mkdir -p build/$$DIR ;\
		mkdir -p build/tmp ;\
		unzip dist/* -d build/tmp ;\
		mv build/tmp/expyriment build/$$DIR ;\
		rm -Rf build/tmp ;\
		rm -Rf build/$$DIR/expyriment/_fonts ;\
		cp -Ra documentation build/$$DIR ;\
		rm -R build/$$DIR/documentation/sphinx/_build  ;\
		cp -a CHANGES.md build/$$DIR ;\
		cp -a COPYING.txt build/$$DIR ;\
		cp -a README.md build/$$DIR ;\
		cp -a setup.py build/$$DIR ;\
		find build/$$DIR -type f -name '*.swp' -o -name '*~' -o -name '*.bak'\
		-o -name '*.py[co]' -o -iname '#*#' | xargs -L 5 rm -f ;\
		cd build ;\
		rm -f $$TAR;\
		tar cfz $$TAR $$DIR;\
		zip -r $$ZIP $$DIR;\
		mv $$TAR ../dist/;\
		mv $$ZIP ../dist/

dist:
	mkdir -p build
	python3 setup.py bdist_wheel --universal | tee build/wheel.log

build/wheel_version: dist 
	@grep "Expyriment Version:" build/wheel.log | awk -F'[' '{print $$2}' \
				| awk -F']' '{print $$1}' > build/wheel_version 

sdist: 
	python3 setup.py sdist

install:
	python3 setup.py install

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
