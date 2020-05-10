import os
import aiomysql
from aiohttp import web
from models.map import Region, Territory


async def start_db_conn(app):
    app['conn'] = await aiomysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            db=os.environ['DB_NAME']
        )


async def close_db_conn(app):
    app['conn'].close()


async def get_all(request):
    game_map = {
            "regions": [],
            "territories": []
            }

    regions = await Region.get_regions(app['conn'])
    territories = await Territory.get_territories(app['conn'])

    for region in regions:
        game_map.get('regions').append(region)

    for territory in territories:
        game_map.get('territories').append(territory)

    return web.json_response(data=game_map)


app = web.Application()
app.add_routes([
    web.get('/v0/map', get_all),
    ])

app.on_startup.append(start_db_conn)


if __name__ == '__main__':
    web.run_app(app)
