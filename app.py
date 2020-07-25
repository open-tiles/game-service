import os
import aiomysql
import behaviour
import aiohttp_cors
from aiohttp import web
import attack as attacking


DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = int(os.environ.get('DB_PORT'))


async def create_db_pool(app):
    app['pool'] = await aiomysql.create_pool(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            port=DB_PORT
        )


async def close_db_conn(app):
    await app['pool'].close()

app = web.Application()
app.on_startup.append(create_db_pool)

cors = aiohttp_cors.setup(app)

resource = cors.add(app.router.add_resource("/v0/attack"))
route = cors.add(
        resource.add_route("PATCH", attacking.hex_attack), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=(
                    "Access-Control-Allow-Origin",
                    "X-Custom-Server-Header"
                    ),
                allow_headers=(
                    "X-Custom",
                    "Access-Control-Allow-Origin",
                    "application/json",
                    "Content-Type"
                    ),
                )
        })

app.add_routes([
        web.get('/v0/board', behaviour.load_board),
        web.get('/v0/check-connection', attacking.check_connection),
        web.patch('/v0/update-tokens', behaviour.update_tokens),
        ])

if __name__ == "__main__":
    web.run_app(app)
