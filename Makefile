GAME_IP=$(shell docker inspect game-service-tiles | grep "\"IPAddress\": \"172")
BOARD_IP=$(shell docker inspect board-api-tiles | grep "\"IPAddress\": \"172")
PLAYER_IP=$(shell docker inspect player-api-tiles | grep "\"IPAddress\": \"172")
COMBAT_IP=$(shell docker inspect combat-api-tiles | grep "\"IPAddress\": \"172")
export DB_HOST?=127.0.0.1
export DB_PASS?=tilesdev
export DB_USER?=tilesdev
export DB_NAME?=tiles
export DB_PORT?=3306
export BOARD_API_URL?=http://localhost:4321
export PLAYER_API_URL?=http://localhost:5432
export COMBAT_API_URL?=http://localhost:6543


ip:
	@echo "game-service: " ${GAME_IP}
	@echo "board-api: " ${BOARD_IP}
	@echo "player-api: " ${PLAYER_IP}
	@echo "combat-api: " ${COMBAT_IP}

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
