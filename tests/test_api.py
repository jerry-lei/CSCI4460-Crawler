import sys
import unittest
sys.path.append('../src')
sys.path.append('../src/crawl')
from src.app import APP

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sample(self):
        assert True
