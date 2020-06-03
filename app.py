import os
import aiohttp
import aiomysql
from aiohttp import web
from models.map import Territory
from models.player import Player


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
        url = f'http://localhost:5432/v0/player/{player_id}'
        async with session.get(url) as resp:
            print(resp.status)
            print(await resp.text())


async def attack(request):

    territory_id = 1
    attacker = None
    async with aiohttp.ClientSession() as session:
        url = f'http://localhost:5432/v0/get?id={territory_id}'
        async with session.get(url) as resp:
            attacker = resp

    territory_id = 2
    defender = None
    async with aiohttp.ClientSession() as session:
        url = f'http://localhost:5432/v0/get?id={territory_id}'
        async with session.get(url) as resp:
            defender = resp

    data = {
            'attacker': attacker,
            'defender': defender
            }

    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:7654/v0/basic-combat'
        async with session.post(url, data=data) as resp:
            print(resp.status)
            print(await resp.text())


async def close_db_conn(app):
    await app['pool'].close()


async def get_all(request):
    territories = await Territory.get_territories(request)
    request.app['territories'] = territories
    return web.json_response(territories)


app = web.Application()

app.on_startup.append(create_db_pool)

app.add_routes([
        web.get('/v0/map', get_all),
        web.post('/v0/attack', Player.attack),
        web.get('/v0/owned', Player.get_owned),
        ])

if __name__ == "__main__":
    web.run_app(app)
