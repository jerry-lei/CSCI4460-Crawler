from datetime import datetime, timedelta

# continuously check to see if any URL is expired
# By expiring it means that the lastUpdated is "frequency" older
def db_scanner(collection):
    item = collection.find_one()
    if not item:
        return []
    d = datetime.today() - timedelta(days = item['frequency'])
    
    #check = 0
    expired_link = []
    for item in collection.find({ "lastUpdated": {"$lte": d}}): # 7 or older
        # if check == 0:
        #     print("Links need to be crawled again:")
        #     check = 1
        expired_link.append(item['url'])

    return expired_link
