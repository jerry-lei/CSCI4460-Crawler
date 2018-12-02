import unittest
import db
import scanner
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta

class TestDB(unittest.TestCase):

    def setUp(self): # test connection to db
        try:
            self.collection = db.connect_db()
        except ConnectionFailure:
            self.collection = -1
        self.assertNotEquals(self.collection, -1)

    def test_insertion(self): # test insertion, 1 for inserting, 0 for dup
        url = "www.bing.com"
        freq = 7
        lastUpdated = datetime.today()
        response = True

        post = db.insertion(self.collection, url, freq, lastUpdated, response)
        
        self.assertTrue(post == 1 or post == 0)

    def test_scanner(self): # test scanner by inserting expired link and find if scanner returns that
        url = "www.yahoo.com"
        freq = 7
        lastUpdated = datetime.today() - timedelta(days = 14)
        response = True

        db.insertion(self.collection, url, freq, lastUpdated, response)        
        expired_link = scanner.db_scanner(self.collection)

        check = False
        for item in expired_link:
            if item == url:
                check = True

        self.assertTrue(check)

if __name__ == '__main__':
    unittest.main()