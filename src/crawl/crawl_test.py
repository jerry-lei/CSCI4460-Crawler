import unittest
from crawler import *
from scheduler import Scheduler
from multiprocessing import Queue
import concurrent.futures

class TestCrawl(unittest.TestCase):

    def setUp(self):
        pass

    def test_good_link(self):
        resp = crawl_link("https://google.com")
        self.assertEqual(resp[1], True)

    def test_bad_link(self):
        resp = crawl_link("https://a.edu")
        self.assertEqual(resp[1], False)

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler(4)
        self.scheduler.start()
        self.link_set1 = ["https://google.com", "https://rpi.edu.com", "https://apple.com", "https://rpi.edu", "https://a.com"]
        self.link_set2 = ["https://lms.rpi.edu", "https://github.com", "https://linkedin.com", "https://facebook.com", "https://albany.edu"]

    def tearDown(self):
        self.scheduler.exit = True

    def test_hp_good_links(self):
        resp = self.scheduler.dump_hp_links(self.link_set2)
        print(resp)
        self.assertEqual(resp["https://lms.rpi.edu"][1], True)
        self.assertEqual(resp["https://github.com"][1], True)
        self.assertEqual(resp["https://linkedin.com"][1], True)
        self.assertEqual(resp["https://facebook.com"][1], True)
        self.assertEqual(resp["https://albany.edu"][1], True)

    def test_hp_bad_links(self):
        resp = self.scheduler.dump_hp_links(self.link_set1)
        print(resp)
        self.assertEqual(resp["https://rpi.edu.com"][1], False)
        self.assertEqual(resp["https://a.com"][1], False)
        self.assertEqual(resp["https://google.com"][1], True)
        self.assertEqual(resp["https://apple.com"][1], True)
        self.assertEqual(resp["https://rpi.edu"][1], True)

    def test_lp_good_links(self):
        resp = self.scheduler.dump_lp_links(self.link_set2)
        print(resp)
        self.assertEqual(resp["https://lms.rpi.edu"][1], True)
        self.assertEqual(resp["https://github.com"][1], True)
        self.assertEqual(resp["https://linkedin.com"][1], True)
        self.assertEqual(resp["https://facebook.com"][1], True)
        self.assertEqual(resp["https://albany.edu"][1], True)

    def test_lp_bad_links(self):
        resp = self.scheduler.dump_lp_links(self.link_set1)
        print(resp)
        self.assertEqual(resp["https://rpi.edu.com"][1], False)
        self.assertEqual(resp["https://a.com"][1], False)
        self.assertEqual(resp["https://google.com"][1], True)
        self.assertEqual(resp["https://apple.com"][1], True)
        self.assertEqual(resp["https://rpi.edu"][1], True)

    def test_hp_priority(self):

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            f1 = executor.submit(self.scheduler.dump_lp_links, self.link_set1)
            f2 = executor.submit(self.scheduler.dump_hp_links, self.link_set2)

            while True:
                if not f1.running() or not f2.running():
                    self.assertEqual(f1.running(), True)
                    self.assertEqual(f2.running(), False)
                    break




if __name__ == '__main__':
    unittest.main()
