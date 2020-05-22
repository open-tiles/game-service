import aiomysql


class Territory:

    def __init__(
            self,
            territory_id,
            name,
            region,
            tokens=0,
            owner=None,
            boardering=[]
            ):
        self.territory_id = territory_id
        self.name = name
        self.region = region
        self.tokens = tokens
        self.owner = owner
        self.boardering = boardering

    async def get_boarders(db_conn, territory_id):
        async with db_conn as conn:
            cur = await conn.cursor(aiomysql.DictCursor)
            query = f'''
            SELECT territories.id, territories.name,
            territories.tokens, territories.owner
            FROM territories
            INNER JOIN boarders ON boarders.territory_to_id = territories.id
            WHERE boarders.territory_from_id = {territory_id}
            '''
            await cur.execute(query)
            boarders = await cur.fetchall()
            b = []
            for territory in boarders:
                x = Territory(
                            territory.get('id'),
                            territory.get('name'),
                            territory.get('region_id'),
                            territory.get('tokens'),
                            territory.get('owner'),
                            )
                b.append(x.__dict__)
            return b

    async def get_territories(request):
        async with request.app['pool'].acquire() as conn:
            cur = await conn.cursor(aiomysql.DictCursor)
            try:
                await cur.execute(f"SELECT * FROM territories")
                territories = await cur.fetchall()
            except Exception as e:
                return {'error': e}
            t = []
            for territory in territories:
                x = Territory(
                        territory.get('id'),
                        territory.get('name'),
                        territory.get('region_id'),
                        territory.get('tokens'),
                        territory.get('owner'),
                        await Territory.get_boarders(
                            request.app['pool'].acquire(),
                            territory.get('id')
                            )
                    )
                t.append(x.__dict__)
            return t


class Boarder:

    def __init__(self, boarder_id, territory_id, tokens, owner):
        self.boarder_id = boarder_id
        self.territory_id = territory_id
        self.tokens = tokens
        self.owner = owner


class Region:

    def __init__(self, region_id, name, ref):
        self.region_id = region_id
        self.name = name
        self.ref = ref

    async def get_regions(request):
        async with request.app['pool'].acquire() as conn:
            cur = await conn.cursor(aiomysql.DictCursor)
            await cur.execute(f"SELECT * FROM regions")
            regions = await cur.fetchall()
            rs = []
            for region in regions:
                rs.append(Region(
                        region.get('id'),
                        region.get('name'),
                        'temp_value'
                        ))
        return rs

