import os
import json
import pytest
import aiomysql
import behaviour


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')


@pytest.fixture
async def pool(loop):
    async with aiomysql.create_pool(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME) as pool:
        yield pool


class FakeURL:

    def __init__(self, queries={}):
        self.query = queries


class FakeRequest():

    def __init__(self, _raise_exception=False, _json=None, app=None, url=None):
        self._json = _json
        self._raise_exception = _raise_exception
        self.app = app or {}
        self.rel_url = url

    async def json(self):
        if self._raise_exception:
            json.loads('None')
        return self._json


async def test_update_tokens():
    response = await behaviour.update_tokens(1000, 2000)
    status = response.status
    assert status == 400


async def test_load_board():
    url = FakeURL({'id': 2})
    request = FakeRequest(url=url)
    response = await behaviour.load_board(request)
    actual = json.loads(response.text)
    expected = {
            "board-info": {
                "id": 2,
                "description": "Test board",
                "created": "2020-07-22 17:53:01",
                "playing": 2,
                "players": [
                    {
                        "id": 1,
                        "username": "Billy-Bob",
                        "created": "2020-07-22 17:53:00",
                        "colour": "#6ed173",
                        "wins": 0,
                        "draws": 0,
                        "losses": 0
                    },
                    {
                        "id": 2,
                        "username": "Zanny-Zaz",
                        "created": "2020-07-22 17:53:01",
                        "colour": "#fa6511",
                        "wins": 0,
                        "draws": 0,
                        "losses": 0
                    }
                ]
            },
            "hexagons": [
                {
                    "hex_id": 10,
                    "player_id": 1,
                    "tokens": 5,
                    "x": 0,
                    "y": 0,
                    "playable": 1,
                    "neighbors": [
                        11
                    ]
                },
                {
                    "hex_id": 11,
                    "player_id": 2,
                    "tokens": 9,
                    "x": 0,
                    "y": 1,
                    "playable": 1,
                    "neighbors": [
                        10
                    ]
                }
            ]
        }
    assert expected == actual
