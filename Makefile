# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: build install clean source_tarball

release: build html_documentation api_ref_html pdf_documentation
	@# requires numpydoc. install: easy_install numpydoc
	make --directory=documentation/sphinx clean
	make --directory=documentation/api clean
	@echo "copy files"
	@mv -f build/lib* build/release
	@cp -ra documentation build/release
	@cp -ra examples build/release
	@cp -at build/release  CHANGES.md COPYING.txt README.md 
	@cp -at build/release  setup.py
	@find build/release -type f -name '*.swp' -o -name '*~' -o -name '*.bak'\
		-o -name '*.py[co]' -o -iname '#*#' | xargs -L 5 rm -f;\

# make zip file from the last release (make release)
zip: build/release
	@read -p "Version: " VER;\
		cd build;\
		ln -s release expyriment-$$VER;\
		rm -f expyriment-$$VER.zip;\
		zip -r expyriment-$$VER.zip expyriment-$$VER;\
		rm expyriment-$$VER;\
		sha1sum expyriment-$$VER.zip
	

# make tarball from the last release (make release)
tarball: build/release 
	@read -p "Version: " VER;\
	 read -p "Tarball version suffix: " VERSION_SUFFIX;\
		cd build;\
		DIR=python-expyriment-$$VER$$VERSION_SUFFIX;\
		cp -ra release $$DIR;\
		rm  $$DIR/expyriment/_fonts -rf;\
		rm  $$DIR/documentation/html -rf;\
		rm  $$DIR/documentation/apt_ref_html -rf;\
		tar cfz $$DIR.orig.tar.gz $$DIR;\
		rm -rf $$DIR;\
		sha1sum $$DIR.orig.tar.gz;\

debian_package:
	read -p "Version: " VER;\
	 	read -p "Tarball version suffix: " VERSION_SUFFIX;\
		cd build;\
		DIR=python-expyriment-$$VER$$VERSION_SUFFIX;\
		tar xfz $$DIR.orig.tar.gz;\
		cd $$DIR;\
		cp ../../debian ./ -ra;\
		debuild -rfakeroot -S ;\
		cd ..;\
		rm -rf $$DIR;

	

build:
	-@rm -rf build/release
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
	@make --directory=documentation/sphinx clean
	@make --directory=documentation/api clean
	@rm -rf build \
			documentation/pdf\
			documentation/api_ref_html\
			documentation/html 
	@find . -name '*.py[co]' \
		 -o -iname '#*#' | xargs -L 10 rm -f
