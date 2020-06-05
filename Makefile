export DB_HOST?=127.0.0.1
export DB_PASS?=admin
export DB_USER?=admin
export DB_NAME?=risk
export DB_PORT?=8765
export BOARD_API_URL?=http://localhost
export PLAYER_API_URL?=http://localhost
export COMBAT_API_URL?=http://localhost
export BOARD_API_PORT?=4321
export PLAYER_API_PORT?=5432
export COMBAT_API_PORT?=6543


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
