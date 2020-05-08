import uuid
from aiohttp import web
from models.map import Territory, Region

r_1 = Region(uuid.uuid4(), "Asia", "region-asia")
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

game_map = {
        "regions": [r_1],
        "territories": [t_1, t_2]
    }


async def on_startup(app):
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
    web.get('/v0/get_all', get_all),
    ])

app.on_startup.append(on_startup)


if __name__ == '__main__':
    web.run_app(app)
