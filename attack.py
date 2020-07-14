import os
import json
import aiohttp
from aiohttp import web

BOARD_API_URL = os.environ.get('BOARD_API_URL')
COMBAT_API_URL = os.environ.get('COMBAT_API_URL')


async def hex_attack(request):
    params = request.rel_url.query
    attacker = await get_hex(params['attacker'])
    defender = await get_hex(params['defender'])
    attacker = json.loads(attacker.text)
    defender = json.loads(defender.text)
    connection = await check_connection(
            attacker.get('hex_id'),
            defender.get('hex_id')
            )
    connection = json.loads(connection.text)
    if connection.get('Connection'):
        result = await basic_combat(attacker, defender)
        if result < 1:
            await change_ownership(
                    attacker.get('player_id'),
                    defender.get('hex_id')
                    )
            x = await update_tokens(result, defender.get('hex_id'))
            return web.json_response(json.loads(x.text))
        else:
            update_tokens(result, defender.get('hex_id'))
        return web.json_response({'attacker': 'lost'})
    return web.json_response({'something': 'else'})


async def check_connection(from_id, to_id):
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}/v0/check-connection?from={from_id}&to={to_id}'
        async with session.get(url) as resp:
            if resp.status == 200:
                return web.json_response(await resp.json())
            return web.json_response(
                    {"error": "check your hex IDs"},
                    status=404
                    )


async def change_ownership(player_id, hex_id):
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}/v0/change-ownership'
        data = {
                'player_id': player_id,
                'hex_id': hex_id
                }
        data = json.dumps(data)
        async with session.patch(url, data=data) as resp:
            if resp.status == 200:
                return web.json_response({'good': 'job'})


async def update_tokens(tokens, hex_id):
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}/v0/update-tokens'
        data = {
                'tokens': tokens,
                'hex_id': hex_id
                }
        data = json.dumps(data)
        async with session.patch(url, data=data) as resp:
            if resp.status == 200:
                return web.json_response(
                        {'winner': ''}, status=200)
            else:
                return web.json_response(
                    {'error': 'something went wrong'})


async def get_hex(hex_id):
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}/v0/get-hex?id={hex_id}'
        async with session.get(url) as resp:
            return web.json_response(await resp.json())


async def basic_combat(attacker, defender):
    data = {
            "attacker": attacker,
            "defender": defender
            }
    data = json.dumps(data)

    async with aiohttp.ClientSession() as session:
        url = f'{COMBAT_API_URL}/v0/basic-combat'
        async with session.post(url, data=data) as resp:
            data = await resp.json()
            tokens = data.get('result')
            return tokens
