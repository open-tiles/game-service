import os
import json
import aiohttp
import aiomysql
from aiohttp import web

BOARD_API_URL = os.environ.get('BOARD_API_URL')
COMBAT_API_URL = os.environ.get('COMBAT_API_URL')
PLAYER_API_URL = os.environ.get('PLAYER_API_URL')
BOARD_API_PORT = os.environ.get('BOARD_API_PORT')
COMBAT_API_PORT = os.environ.get('COMBAT_API_PORT')
PLAYER_API_PORT = os.environ.get('PLAYER_API_PORT')


async def create_db_pool(app):
    app['pool'] = await aiomysql.create_pool(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            db=os.environ['DB_NAME'],
            port=int(os.environ['DB_PORT'])
        )


async def get_players(request):
    async with aiohttp.ClientSession() as session:
        player_id = 1
        url = f'{PLAYER_API_URL}:{PLAYER_API_PORT}/v0/player/{player_id}'
        async with session.get(url) as resp:
            print(resp.status)
            print(await resp.text())


async def get_territory(territory_id):
    territory = None
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}:{BOARD_API_PORT}/v0/get-territory?territory_id={territory_id}'
        async with session.get(url) as resp:
            data = await resp.json()
            territory = data
    return territory


async def attack(request):
    params = request.rel_url.query
    attacker_id = params['attacker']
    defender_id = params['defender']

    attacker = await get_territory(str(attacker_id))
    defender = await get_territory(str(defender_id))

    data = {
            "attacker": attacker,
            "defender": defender
            }
    data = json.dumps(data)

    async with aiohttp.ClientSession() as session:
        url = f'{COMBAT_API_URL}:{COMBAT_API_PORT}/v0/basic-combat'
        async with session.post(url, data=data) as resp:
            data = await resp.json()
        return web.json_response(data)


async def close_db_conn(app):
    await app['pool'].close()


app = web.Application()

app.on_startup.append(create_db_pool)

app.add_routes([
        web.get('/v0/attack', attack),
        ])

if __name__ == "__main__":
    web.run_app(app)
