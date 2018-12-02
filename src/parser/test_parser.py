import unittest
import parser

class TestParser(unittest.TestCase):

    def test_basic_page(self):
        expected_result = ['/cgi-bin/', '/rcs/', '/~sibel/poetry/poems/', '/~sibel/poetry/books/', '/~musser/dagproc']
        self.assertEqual(parser.get_bad_paths("http://cs.rpi.edu/robots.txt"), expected_result)

    def test_nonexistent_page(self):
        self.assertEqual(parser.get_bad_paths("http://rpi.edu/robots.taxt"), [])

    def test_targeted_disallows(self):
        expected_result = ['/feed/', '/c/accounts/', '/c/crontab/', '/c/graphics/', '/c/locale/', '/c.new/', '/c.bak/', '/c_hacks', '/c/pinc/', '/c/setup/', '/c/stats/', '/c/tools/', '/c/users/', '/down/', '/dpmail/', '/d', '/out', '/jpgraph/', '/jpgraph-1.14', '/archive', '/projects', '/mailman/', '/noncvs', '/phpbb2', '/phpbb3', '/phpbb-3.2.0', '/phpmyadmin', '/sawiki', '/squirrels', '/stats/', '/tools', '/w', '/wikiheiro']
        self.assertEqual(parser.get_bad_paths("https://www.pgdp.net/robots.txt"), expected_result)

    def test_allows(self):
        self.assertEqual(parser.get_bad_paths("https://www.choiceofgames.com/robots.txt"), [])

if __name__ == "__main__":
    unittest.main()
