export DB_HOST?=127.0.0.1
export DB_PASS?=admin
export DB_USER?=admin
export DB_NAME?=risk
export DB_PORT?=8765
export BOARD_API_URL?=localhost
export COMBAT_API_URL?=localhost
export PLAYER_API_URL?=localhost


up:
	docker-compose up -d

run: 
	python app.py

test:
	pytest

dev-run:
	adev runserver .

install: install-test
	pip install -r requirments

install-test: pip install -r requirements-test
