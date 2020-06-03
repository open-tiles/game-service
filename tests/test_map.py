import pytest
import aiohttp
from models.map import Boarders
from unittest.mock import Mock


class FakeRequest():

    def __init(self, data=None):
        self.data = data


async def test_get_baorders():
    assert True
