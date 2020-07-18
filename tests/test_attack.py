import json
import attack


class FakeURL():

    def __init__(self, queries={}):
        self.query = queries


class FakeRequest():

    def __init__(self, _raise_exception=False, _json=None, app=None, url=None):
        self._raise_exception = _raise_exception
        self._json = _json
        self.app = app or {}
        self.url = url

    async def json(self):
        if self._raise_exception:
            json.loads('None')
        return self._json


async def test_attack():
    request = FakeRequest()
    await attack.hex_attack(request)
