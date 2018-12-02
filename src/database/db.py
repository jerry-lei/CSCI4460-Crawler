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

    except Exception:
            print("Duplicates, do nothing")

# print all item in the db
def print_all(collection):
    for item in collection.find():
        pprint.pprint(item)

# find and print the item with certain attribute
def find_all(collection, attri):
    for item in collection.find({"url": attri}):
        pprint.pprint(item)

# find and print the item, since it contains no duplicate, can just use find_one
def find_unique(collection, url):
    pprint.pprint(collection.find_one({"url": url}))

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

"""
if __name__ == "__main__":
    # insertion/posting
    url = "www.bing.com"
    freq = 7
    lastUpdated = datetime.today()
    response = True

    # connect to db
    collection = connect_db()

    # insert using today's date
    insertion(collection, url, freq, lastUpdated, response)
    
    # insert using 14 days earlier than today
    url = "www.yahoo.com"
    lastUpdated = datetime.today() - timedelta(days = 14)
    insertion(collection, url, freq, lastUpdated, response)

    # test 
    #print_all(collection) # print all item in the db
    #find_unique(collection, "www.bing.com")
    db_scanner(collection)"""