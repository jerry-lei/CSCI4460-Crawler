"""
    This script starts a connection to the database and provides
    neccessary functions for managing.

"""
import pymongo
import pprint
from pymongo import MongoClient
from datetime import datetime, timedelta

# Insert to db and doesn't allow duplicate insertion
def insertion(collection, url, freq, lastUpdated, response):
    post = {"url": url,
            "frequency": freq,
            "lastUpdated": lastUpdated,
            "Response": response}

    # insert if and only if the item isn't already existed in the db
    try:
        post_id = collection.insert_one(post).inserted_id # unique key
        print("Inserted")
        print("post_id", post_id)
        return 1

    except Exception:
        print("Duplicates, do nothing")
        return 0


# connects to local database
def connect_db():
    # connect to local database
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    client = MongoClient('mongodb://localhost:27017/')

    # setup database and collection
    db = client.database
    collection = db.collection

    db.collection.create_index([('url', pymongo.ASCENDING)], unique=True)
    return collection