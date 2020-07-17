import behaviour


async def test_update_turn():
    pass


async def test_update_tokens():
    response = await behaviour.update_tokens(1000, 2000)
    status = response.status
    assert status == 400


async def test_load_board():
    pass
