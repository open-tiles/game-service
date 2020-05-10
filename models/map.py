import aiomysql

class Territory:

    def __init__(
            self,
            tid,
            name,
            region,
            tokens=0,
            owner=None,
            boarders={}
            ):
        self.tid = tid
        self.name = name
        self.region = region
        self.tokens = tokens
        self.owner = owner
        self.boarders = boarders

    def json(self):
        territory = {
            "tid": str(self.tid),
            "name": self.name,
            "tokens": self.tokens,
            "owner": self.owner,
            "boarders": self.boarders,
            "region": self.region.json(),
            }
        return territory

    async def get_territories(conn):
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute("SELECT * FROM Territories")
        territories = await cur.fetchall()
        await cur.close()
        return territories


class Region:

    def __init__(self, rid, name, ref):
        self.rid = rid
        self.name = name
        self.ref = ref

    def json(self):
        region = {
                "rid": str(self.rid),
                "name": self.name,
                "ref": self.ref
                }
        return region

    async def get_regions(conn):
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute("SELECT * FROM Regions")
        regions = await cur.fetchall()
        await cur.close()
        return regions
