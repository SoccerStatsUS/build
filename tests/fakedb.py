"""A minimal in-memory stand-in for the mongo handle the build stages use.

The stages reach for a module-global `soccer_db` and drop/refill whole
collections. Only the handful of operations they actually call are implemented.
"""


class FakeCollection:
    def __init__(self, rows=()):
        self.rows = [dict(r) for r in rows]

    def find(self, spec=None):
        for row in self.rows:
            if spec is None or all(row.get(k) == v for k, v in spec.items()):
                yield dict(row)

    def insert_one(self, row):
        self.rows.append(dict(row))

    def drop(self):
        self.rows = []

    def estimated_document_count(self):
        return len(self.rows)


class FakeDB:
    """Addressable both as soccer_db['x_games'] and soccer_db.standings."""

    def __init__(self, **collections):
        self._colls = {name: FakeCollection(rows) for name, rows in collections.items()}

    def __getitem__(self, name):
        return self._colls.setdefault(name, FakeCollection())

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        return self[name]
