import os
import aiohttp
import aiomysql
from aiohttp import web


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


async def get_territory(territory_id):
    territory = None
    async with aiohttp.ClientSession() as session:
        url = f'http://localhost:5432/v0/get?id={territory_id}'
        async with session.get(url) as resp:
            territory = resp
    return territory


async def attack(request):
    params = request.rel_url.query
    attacker_id = params['attacker']
    defender_id = params['defender']

    attacker = get_territory(attacker_id)
    defender = get_territory(defender_id)

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


app = web.Application()

app.on_startup.append(create_db_pool)

app.add_routes([
        web.post('/v0/attack', attack),
        ])

if __name__ == "__main__":
    web.run_app(app)
