from aiohttp import web


class Player:

    def __init__(self, pid, name, tiles):
        self.pid = pid
        self.name = name
        self.tiles = tiles

    async def attack(request):
        data = await request.json()
        territories = {
                'France': 11,
                'UK': 20
                }
        at = territories[data['attacker']]
        dt = territories[data['defender']]
        print(at - dt)
        return web.json_response()
