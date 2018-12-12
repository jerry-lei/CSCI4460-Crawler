'''
    This contains tests for the parse and get_bad_paths methods.
'''

import unittest
import parser

class TestParser(unittest.TestCase):
    '''
        This contains tests for the parse and get_bad_paths methods.
    '''

    def test_empty(self):
        ''' Parse an empty string.'''
        self.assertEqual(parser.parse(''), [])

    def test_one_disallow(self):
        ''' Parse a string with one disallow.'''
        self.assertEqual(parser.parse("Disallow: /stuff/"), ['/stuff/'])

    def test_two_disallows(self):
        ''' Parse a string with two disallows.'''
        self.assertEqual(parser.parse("Disallow: /stuff/\nDisallow:   /home/"), ['/stuff/', '/home/'])

    def test_allow(self):
        ''' Parse an string with an allow statemnt.'''
        self.assertEqual(parser.parse("Allow: /stuff/"), [])

    def test_applicable_useragent(self):
        ''' Parse a string with a user-agent and a relevant disallow.'''
        self.assertEqual(parser.parse("User-agent: * \nDisallow: /stuff/"), ['/stuff/'])

    def test_not_applicable_useragent(self):
        ''' Parse a string with an unknown user-agent and a disallow that is ignored.'''
        self.assertEqual(parser.parse("User-agent: someone else \nDisallow: /stuff/"), [])

    def test_basic_page(self):
        ''' Test a simple robots.txt page. '''
        expected_result = ['/cgi-bin/', '/rcs/', '/~sibel/poetry/poems/', '/~sibel/poetry/books/', '/~musser/dagproc']
        self.assertEqual(parser.get_bad_paths("http://cs.rpi.edu/robots.txt"), expected_result)

    def test_nonexistent_page(self):
        ''' Test a page that doesn't exist.'''
        self.assertEqual(parser.get_bad_paths("http://rpi.edu/robots.taxt"), [])

    def test_targeted_disallows(self):
        ''' Test a page that has targeted disallows.'''
        expected_result = ['/feed/', '/c/accounts/', '/c/crontab/', '/c/graphics/', '/c/locale/', '/c.new/', '/c.bak/', '/c_hacks', '/c/pinc/', '/c/setup/', '/c/stats/', '/c/tools/', '/c/users/', '/down/', '/dpmail/', '/d', '/out', '/jpgraph/', '/jpgraph-1.14', '/archive', '/projects', '/mailman/', '/noncvs', '/phpbb2', '/phpbb3', '/phpbb-3.2.0', '/phpmyadmin', '/sawiki', '/squirrels', '/stats/', '/tools', '/w', '/wikiheiro']
        self.assertEqual(parser.get_bad_paths("https://www.pgdp.net/robots.txt"), expected_result)

    def test_allows(self):
        ''' Test a page that has allows.'''
        self.assertEqual(parser.get_bad_paths("https://www.choiceofgames.com/robots.txt"), [])


if __name__ == "__main__":
    unittest.main()
