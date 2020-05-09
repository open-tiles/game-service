import os
import uuid
import aiomysql
from aiohttp import web
from models.map import Territory, Region

r_1 = Region(uuid.uuid4(), "Asia", "region-asia")
r_2 = Region(uuid.uuid4(), "Europe", "region-europe")
t_1 = Territory(
        uuid.uuid4(),
        "China",
        r_1,
        )
t_2 = Territory(
        uuid.uuid4(),
        "Japan",
        r_1,
        )
t_3 = Territory(
        uuid.uuid4(),
        "United Kingdom",
        r_2,
        )
game_map = {
        "regions": [r_1, r_2],
        "territories": [t_1, t_2, t_3]
    }


async def on_startup(app):
    app['conn'] = await aiomysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            db=os.environ['DB_NAME']
        )
    pass


async def get_all(request):
    data = {
            "regions": [],
            "territories": []
            }
    for region in game_map.get("regions"):
        data.get("regions").append(region.get())

    for territory in game_map.get("territories"):
        data.get("territories").append(territory.get())

    return web.json_response(data=data)


app = web.Application()
app.add_routes([
    web.get('/v0/map', get_all),
    ])

app.on_startup.append(on_startup)


if __name__ == '__main__':
    web.run_app(app)
