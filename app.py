import os
import json
import aiohttp
import aiomysql
from aiohttp import web

BOARD_API_URL = os.environ.get('BOARD_API_URL')
COMBAT_API_URL = os.environ.get('COMBAT_API_URL')
PLAYER_API_URL = os.environ.get('PLAYER_API_URL')
DB_HOST = os.environ.get('DB_HOST')

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = int(os.environ('DB_PORT'))


async def create_db_pool(app):
    app['pool'] = await aiomysql.create_pool(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            port=DB_PORT
        )


async def get_players(request):
    async with aiohttp.ClientSession() as session:
        player_id = 1
        url = f'{PLAYER_API_URL}/v0/player/{player_id}'
        async with session.get(url) as resp:
            return await resp.text()


async def get_territory(territory_id):
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}/v0/get-territory?territory_id={territory_id}'
        async with session.get(url) as resp:
            return await resp.json()


async def attack(request):
    params = request.rel_url.query
    attacker_id = params['attacker']
    defender_id = params['defender']

    attacker = await get_territory(attacker_id)
    defender = await get_territory(defender_id)

    if attacker.get('error'):
        return web.json_response(attacker, status=404)
    if defender.get('error'):
        return web.json_response(defender, status=404)

    attacking_player_id = attacker.get('owner')
    if attacking_player_id == 'Null':
        return web.json_response(
                {'error': 'attacking territory is not owned by any player'}
                )

    data = {
            "attacker": attacker,
            "defender": defender
            }
    data = json.dumps(data)

    async with aiohttp.ClientSession() as session:
        url = f'{COMBAT_API_URL}/v0/basic-combat'
        async with session.post(url, data=data) as resp:
            data = await resp.json()
        # return web.json_response(data)

    if data.get('result') < 1:
        async with aiohttp.ClientSession() as session:
            url = f'{BOARD_API_URL}/v0/change-ownership'
            data = {
                    'territory_id': defender_id,
                    'player_id': attacking_player_id
                    }
            data = json.dumps(data)
            async with session.patch(url, data=data) as resp:
                if resp.status == 200:
                    return web.Response(text='we did it', status=200)
                else:
                    return web.json_response({'error': 'something went wrong'})
    else:
        return web.json_response({'result': 'attacker defeated'})


async def close_db_conn(app):
    await app['pool'].close()


app = web.Application()

app.on_startup.append(create_db_pool)

app.add_routes([
        web.get('/v0/attack', attack),
        ])

if __name__ == "__main__":
    web.run_app(app)
