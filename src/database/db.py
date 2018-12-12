"""
    This script starts a connection to the database and provides
    neccessary functions for managing.

"""
import pymongo
from pymongo import MongoClient

def insertion(collection, url, freq, last_updated, response):
    """
        Insert to database and doesn't allow duplicate insertion
    """
    post = {"url": url,
            "frequency": freq,
            "last_updated": last_updated,
            "Response": response}

    # insert if and only if the item isn't already existed in the database
    try:
        post = collection.insert_one(post).inserted_id # unique key
        #print("Inserted")
        #print("post_id", post_id)
        return 1

    except Exception:
        #print("Duplicates, do nothing")
        return 0


def connect_db():
    """
        connects to local database
    """
    # connect to local database
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    client = MongoClient('mongodb://localhost:27017/')

    # setup database and collection
    database = client.database
    collection = database.collection

    database.collection.create_index([('url', pymongo.ASCENDING)], unique=True)
    print(database.collection_names(include_system_collections=False))
    return collection
    