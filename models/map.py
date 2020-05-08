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

    def get(self):
        territory = {
            "tid": str(self.tid),
            "name": self.name,
            "tokens": self.tokens,
            "owner": self.owner,
            "boarders": self.boarders,
            "region": self.region.get(),
            }
        return territory


class Region:

    def __init__(self, rid, name, ref):
        self.rid = rid
        self.name = name
        self.ref = ref

    def get(self):
        region = {
                "rid": str(self.rid),
                "name": self.name,
                "ref": self.ref
                }
        return region
