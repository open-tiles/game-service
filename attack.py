import os
import json
import aiohttp
from aiohttp import web

BOARD_API_URL = os.environ.get('BOARD_API_URL')
COMBAT_API_URL = os.environ.get('COMBAT_API_URL')


async def test_handler(request):
    return web.json_response(
            {"my": "json"},
            status=200
            )


async def hex_attack(request):
    data = await request.json()
    attacker_id = data.get('attacker').get('hex-id')
    defender_id = data.get('defender').get('hex-id')
    attacker = await get_hex(attacker_id)
    defender = await get_hex(defender_id)
    attacker = json.loads(attacker.text)
    defender = json.loads(defender.text)
    connection = await check_connection(attacker_id, defender_id)
    connection = json.loads(connection.text)
    if connection.get('Connection'):
        report = await basic_combat(attacker, defender)
        if report['combatReport'].get('success'):
            await change_ownership(
                    attacker.get('player_id'),
                    defender.get('hex_id')
                    )
            await update_tokens(1, defender.get('hex_id'))
            return web.json_response(
                    report,
                    status=200
                    )
        else:
            update_tokens(1, defender.get('hex_id'))
            return web.json_response(
                    report,
                    status=200
                    )
    return web.json_response(
            {'Result': 'No connection'},
            status=200
            )


async def check_connection(from_id, to_id):
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}/v0/check-connection?from={from_id}&to={to_id}'
        async with session.get(url) as resp:
            if resp.status == 200:
                return web.json_response(
                        await resp.json(),
                        )
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
                return web.json_response(
                        {'good': 'job'},
                        status=200)


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
                        {'winner': 'eeeeeee'},
                        status=200)
            else:
                return web.json_response(
                    {'error': 'something went wrong'},
                    )


async def get_hex(hex_id):
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}/v0/get-hex?id={hex_id}'
        async with session.get(url) as resp:
            return web.json_response(
                    await resp.json(),
                )


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
            return data
