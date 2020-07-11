import os
import json
import aiohttp
from aiohttp import web

BOARD_API_URL = os.environ.get('BOARD_API_URL')


async def update_turn(next_player, board_id):
    url = f'{BOARD_API_URL}/v0/update-turn'
    data = {
            'next': next_player,
            'id': board_id
            }
    data = json.dumps(data)
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, data=data) as resp:
            data = await resp.json()
            return web.json_response(data)
