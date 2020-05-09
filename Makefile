export DB_HOST?=127.0.0.1
export DB_PASS?=admin123
export DB_USER?=admin123
export DB_NAME?=risk
export DB_PORT?=1234


test:
	pytest

run: 
	python app.py

dev-run:
	mysql -h ${DB_HOST} -u ${DB_USER} -p${DB_PASS} &
	adev runserver

install: install-test
	pip install -r requirments

install-test: pip install -r requirements-test
