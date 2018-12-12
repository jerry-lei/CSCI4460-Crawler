"""
    This script starts a scanner that scans through the database
    to check expired links

"""

from datetime import datetime, timedelta

def db_scanner(collection):
    """
        continuously check to see if any URL is expired
        By expiring it means that the last_updated is "frequency" older

    """
    item = collection.find_one()
    if not item:
        return []
    date = datetime.today() - timedelta(days=item['frequency'])
    #check = 0
    expired_link = []
    for item in collection.find({"last_updated":{"$lte":date}}): # 7 or older
        # if check == 0:
        #     print("Links need to be crawled again:")
        #     check = 1
        expired_link.append(item['url'])

    return expired_link
    