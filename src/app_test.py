import unittest
from unittest.mock import MagicMock
import app

class MockHttpResponse:
    def read(self):
        return "test"

class TestSendRequests(unittest.TestCase):
    def setUp(self):
        self.app_instance = app
        self.app_instance.insertion = MagicMock(name='insertion')

    def test_one_bad(self):
        test_object_http_response = MockHttpResponse()
        test_object = {
            "https://www.google.com": [test_object_http_response, True, ""],
            "bad_url": [None, False, ""]
        }
        self.assertEqual(self.app_instance.send_requests(test_object), ['bad_url'])

    def test_none_bad(self):
        test_object_http_response = MockHttpResponse()
        test_object = {
            "https://www.google.com": [test_object_http_response, True, ""],
            "https://www.yahoo.com": [test_object_http_response, True, ""]
        }
        self.assertEqual(self.app_instance.send_requests(test_object), [])

    def test_both_bad(self):
        test_object = {
            "bad_url1": [None, False, ""],
            "bad_url2": [None, False, ""]
        }
        self.assertEqual(self.app_instance.send_requests(test_object), ['bad_url1', 'bad_url2'])

class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        app.APP.testing = True
        self.test_app = app.APP.test_client()
        app.set_up_api()

    def test_bad_robots_request(self):
        rv = self.test_app.get('/robots')
        self.assertIn(b'Bad Request: Bad URL Sent', rv.data)
        self.assertEqual(rv.status_code, 400)
        rv = self.test_app.get('/robots?url=bad_url')
        self.assertEqual(rv.status_code, 400)
        self.assertIn(b'Bad Request: Bad URL Sent', rv.data)

    def test_bad_crawl_request(self):
        rv = self.test_app.post('/crawl', data = dict(
            urls=""
        ))
        self.assertEqual(rv.status_code, 400)
        self.assertIn(b'Bad Request: No URLS key found', rv.data)



if __name__ == "__main__":
    unittest.main()