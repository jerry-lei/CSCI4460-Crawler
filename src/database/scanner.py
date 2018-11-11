from datetime import datetime, timedelta

# continuously check to see if any URL is expired
# By expiring it means that the lastUpdated is "frequency" older
def db_scanner(collection):
    item = collection.find_one()
    #print("item" ,item['lastUpdated'])
    d = datetime.today() - timedelta(days = item['frequency'])
    #print(d)
    
    check = 0
    for item in collection.find({ "lastUpdated": {"$lte": d}}):
        #pprint.pprint(item)
        if check == 0:
            print("Links need to be crawled again:")
            check = 1

        print(item['url'])
