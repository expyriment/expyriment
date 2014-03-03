# Makefile for Expyriment
# (c) Florian Krause <florian@expyriment.org> &
# 	  Oliver Lindemann <oliver@expyriment.org>

.PHONY: build install clean debian_package

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

debian_package:
	@echo "Note: Don't forget to 'make release' before";\
		read -p "Version: " VER;\
		read -p "Version suffix: " SUFFIX;\
		rm build/debian/ -rf;\
		mkdir -p build/debian;\
		cd build/debian;\
		cp ../expyriment-$$VER ./python-expyriment-$$VER$$SUFFIX -ra;\
		rm python-expyriment-$$VER$$SUFFIX/expyriment/_fonts -rf;\
		tar cfz python-expyriment_$$VER$$SUFFIX.orig.tar.gz python-expyriment-$$VER$$SUFFIX;\
		cd python-expyriment-$$VER$$SUFFIX/;\
		cp ../../../debian ./ -ra;\
		debuild -S ;\
		cd ..;\


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
