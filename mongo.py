# Simple mongo functions.

import pymongo

connection = pymongo.MongoClient()
# connection = pymongo.Connection()
soccer_db = connection.soccer

def insert_row(collection, row):
    collection.insert(row)

def insert_rows(collection, rows):
    for row in rows:
        try:
            insert_row(collection, row)
        except:
            #import pdb; pdb.set_trace()
            print("Insert error")
            print(row)
    
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
