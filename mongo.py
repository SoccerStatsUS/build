# Simple mongo functions.

from itertools import islice

import pymongo
from pymongo.errors import BulkWriteError

connection = pymongo.MongoClient()
soccer_db = connection.soccer


def insert_rows(collection, rows, chunk=1000):
    """
    One insert_many per chunk rather than an insert_one per row: the round
    trip, not the parsing, was 95% of a build. Rows mongo rejects are printed
    and the rest of the chunk still lands.
    """
    rows = iter(rows)
    while batch := list(islice(rows, chunk)):
        try:
            collection.insert_many(batch, ordered=False)
        except BulkWriteError as e:
            for err in e.details['writeErrors']:
                print("Insert error: %s" % err['errmsg'])
                print(batch[err['index']])


def get_rows(collection):
    return [row for row in collection.find()]


def generic_load(coll, func, delete=False):
    """
    Call with something like
    
    generic_load(soccer_db.fbleague_scores, fbleague.scrape_all_seasons)
    """
    if delete:
        coll.drop()

    # Allow for non-callable inserts as well.
    if '__call__' in dir(func):
        insert_rows(coll, func())
    else:
        insert_rows(coll, func)
