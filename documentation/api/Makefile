venv:
	python -m venv venv
	venv/bin/pip install flit
	venv/bin/flit -f ../../pyproject.toml install

html: venv
	mkdir -p _build
	venv/bin/python create_api_reference.py
	mv *.html _build
	rm *.pyc -f

clean:
	rm -rf _build
	rm -rf venv
	rm *.html

