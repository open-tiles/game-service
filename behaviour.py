import os
import json
import aiohttp
from aiohttp import web

BOARD_API_URL = os.environ.get('BOARD_API_URL')
PLAYER_API_URL = os.environ.get('PLAYER_API_URL')

headers = {"Access-Control-Allow-Origin": "*"}


async def update_turn(next_player, board_id):
    url = f'{BOARD_API_URL}/v0/update-turn'
    data = {
            'next': next_player,
            'id': board_id
            }
    data = json.dumps(data)
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, data=data) as resp:
            data = await resp.json()
            return web.json_response(
                    data,
                    headers=headers,
                    status=200
                    )


async def players_on_board(board_id):
    url = f'{PLAYER_API_URL}/v0/board-players?id={board_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                players = await resp.json()
                return web.json_response(players)


async def get_board(board_id):
    url = f'{BOARD_API_URL}/v0/get-board?id={board_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                players = await resp.json()
                return web.json_response(players)


async def load_board(request):
    params = request.rel_url.query
    board_id = params['id']
    players = await players_on_board(board_id)
    board = await get_board(board_id)
    players = json.loads(players.text)
    board = json.loads(board.text)
    board['board-info']['players'] = players
    return web.json_response(
            board,
            headers=headers,
            status=200
            )


async def update_tokens(tokens, defender_id):
    async with aiohttp.ClientSession() as session:
        url = f'{BOARD_API_URL}/v0/add-tokens'
        data = {
                'tokens': tokens,
                'territory_id': defender_id
                }
        async with session.patch(url, data=data) as resp:
            if resp.status == 200:
                return web.Response(
                    text='we did it', status=200)
            else:
                return web.json_response(
                    {'error': 'something went wrong'}, status=400)
