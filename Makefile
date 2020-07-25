export DB_HOST?=127.0.0.1
export DB_PASS?=tilesdev
export DB_USER?=tilesdev
export DB_NAME?=tiles
export DB_PORT?=3306
export BOARD_API_URL?=http://localhost:4321
export PLAYER_API_URL?=http://localhost:5432
export COMBAT_API_URL?=http://localhost:6543


branch:
	git branch --show-current
	
up:
	docker-compose pull
	docker-compose up -d

run:
	python app.py

test:
	pytest

down:
	docker-compose down

dev-run:
	adev runserver .

install: install-test
	pip install -r requirements

install-test:
	pip install -r requirements-test
