test:
	pytest

run: 
	python app.py

install: install-test
	pip install -r requirments

install-test: pip install -r requirements-test
