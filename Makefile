# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: install clean

html_documentation: documentation/html
pdf_documentation: documentation/pdf
api_ref_html: documentation/api_ref_html
build: build/release

CLI_SCRIPT=test
override_dh_install:
	echo "#!/bin/sh" > $(CLI_SCRIPT)
	echo "set -e" >> $(CLI_SCRIPT)
	echo -n "python -m expyriment.cli \$$* |" >> $(CLI_SCRIPT) 
	echo "sed 's/ python -m expyriment.cli / expyriment /g'" >> $(CLI_SCRIPT)
	chmod 755 $(CLI_SCRIPT)


build/release: documentation/html documentation/pdf documentation/api_ref_html
	python setup.py build
	make --directory=documentation/sphinx clean
	make --directory=documentation/api clean
	@mv -f build/lib* build/release
	@cp -ra documentation build/release
	@cp -ra examples build/release
	@cp -at build/release  CHANGES.md COPYING.txt README.md
	@cp -at build/release  setup.py
	@python -c "from setup import *; print get_version()+'~'+get_revision()" >\
					build/release.version
	@find build/release -type f -name '*.swp' -o -name '*~' -o -name '*.bak'\
		-o -name '*.py[co]' -o -iname '#*#' | xargs -L 5 rm -f

zip: build/release
	@cd build;\
		VER=$$(cat release.version);\
		ln -s release expyriment-$$VER;\
		rm -f expyriment-$$VER.zip;\
		zip -r expyriment-$$VER.all.zip expyriment-$$VER;\
		rm expyriment-$$VER;\
		sha1sum expyriment-$$VER.all.zip

tarball: build/release
	@cd build;\
		VER=$$(cat release.version);\
	 	read -p "Tarball version suffix: " VERSION_SUFFIX;\
		DIR=python-expyriment-$$VER$$VERSION_SUFFIX;\
		TAR=python-expyriment_$$VER$($VERSION_SUFFIX).orig.tar.gz;\
		cp -ra release $$DIR;\
		rm  $$DIR/expyriment/_fonts -rf;\
		rm  $$DIR/documentation/html -rf;\
		rm  $$DIR/documentation/Expyriment.pdf -rf;\
		rm  $$DIR/documentation/api_ref_html -rf;\
		tar cfz $$TAR $$DIR;\
		rm -rf $$DIR;\
		sha1sum $$TAR

debian_package:
	@cd build;\
		VER=$$(cat release.version);\
	 	read -p "Tarball version suffix: " VERSION_SUFFIX;\
		DIR=python-expyriment-$$VER$$VERSION_SUFFIX;\
		TAR=python-expyriment_$$VER$($VERSION_SUFFIX).orig.tar.gz;\
		rm $$DIR -rf;\
		tar xfz $$TAR;\
		cd $$DIR;\
		cp ../../debian ./ -ra;\
		debuild -rfakeroot -S ;\
		cd ..;\
		#rm -rf $$DIR;	

install:
	python setup.py install

documentation/html:
	make --directory=documentation/sphinx rst html
	mv documentation/sphinx/_build/html documentation/html

documentation/pdf:
	make --directory=documentation/sphinx rst latexpdf
	mv documentation/sphinx/_build/latex/Expyriment.pdf documentation/

documentation/api_ref_html:
	make --directory=documentation/api html
	mv documentation/api/_build documentation/api_ref_html

clean:
	@make --directory=documentation/sphinx clean
	@make --directory=documentation/api clean
	@rm -rf build \
			documentation/Expyriment.pdf\
			documentation/api_ref_html\
			documentation/html
	@find . -name '*.py[co]' \
		 -o -iname '#*#' | xargs -L 10 rm -f
