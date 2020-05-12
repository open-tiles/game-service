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

    def json(self):
        territory = {
            "id": self.territory_id,
            "name": self.name,
            "tokens": self.tokens,
            "owner": self.owner,
            "boarders": self.boarders,
            "region": self.region,
            }
        return territory

    def set_boardering(self, territory):
        self.boardering.append(territory)
        return True

    def dict_to_territory_list(territories):
        territories = list()
        for territory in territories:
            territories.append(
                    Territory(
                        territory.get('TID'),
                        territory.get('Name'),
                        territory.get('RID'),
                        territory.get('Tokens'),
                        territory.get('Owner'),
                        )
                    )
            return territories

    async def get_territories(request):
        territories = await get_all(request, 'territories')
        return territories


class Region:

    def __init__(self, region_id, name, ref):
        self.region_id = region_id
        self.name = name
        self.ref = ref

    def json(self):
        region = {
                "id": self.region_id,
                "name": self.name,
                "ref": self.ref
                }
        return region

    async def get_regions(request):
        regions = await get_all(request, 'regions')
        return regions


class Boarders:

    def __init__(self, from_id, to_id):
        self.from_id = from_id
        self.to_id = to_id

    async def get_boardering_territories(self, request, territory_id):
        async with request.app['pool'].acquire() as conn:
            cur = await conn.cursor(aiomysql.DictCursor)
            query = f'''SELECT territories.id, territories.name,
            territories.tokens, territories.owner
            FROM territories
            INNER JOIN boarders ON boarders.territory_from_id = territories.id
            WHERE boarders.territory_from_id = {territory_id}'''
            await cur.execute(query)
            territories = await cur.fetchall()
            return territories


async def get_all(request, table):
    async with request.app['pool'].acquire() as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(f"SELECT * FROM {table}")
        territories = await cur.fetchall()
    return territories
