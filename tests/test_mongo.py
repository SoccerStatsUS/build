from pymongo.errors import BulkWriteError

from build.mongo import insert_rows
from fakedb import FakeCollection


class RecordingCollection(FakeCollection):
    def __init__(self):
        super().__init__()
        self.batches = []

    def insert_many(self, rows, ordered=True):
        self.batches.append(len(rows))
        super().insert_many(rows)


def test_inserts_in_chunks_from_any_iterable():
    coll = RecordingCollection()
    insert_rows(coll, ({'n': i} for i in range(2500)), chunk=1000)
    assert coll.batches == [1000, 1000, 500]
    assert [r['n'] for r in coll.rows] == list(range(2500))


def test_empty_input_makes_no_call():
    coll = RecordingCollection()
    insert_rows(coll, [])
    assert coll.batches == []


def test_rejected_rows_are_reported_and_the_rest_land(capsys):
    class Rejecting(FakeCollection):
        def insert_many(self, rows, ordered=True):
            good = [r for r in rows if r['n'] != 1]
            super().insert_many(good)
            raise BulkWriteError({'writeErrors': [{'index': 1, 'errmsg': 'duplicate key'}]})

    coll = Rejecting()
    insert_rows(coll, [{'n': 0}, {'n': 1}, {'n': 2}])
    assert [r['n'] for r in coll.rows] == [0, 2]
    out = capsys.readouterr().out
    assert 'duplicate key' in out
    assert "{'n': 1}" in out
