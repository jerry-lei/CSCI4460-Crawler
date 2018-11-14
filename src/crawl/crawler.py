""" This script the function to crawl links.


Good test cases & their behaviors:

https://.com -- crawl_link returns an error -- none of the excepts catch this
https://rpi.edu.com -- takes a long time to respond

"""


import urllib.request
import validators
from urllib.error import URLError, HTTPError, ContentTooShortError


def crawl_link(link):
    """ Crawls a link, and returns a tuple with a urllib response and a code
        indicating success or error

    Input:
        string -- link to be claled

    Returns:
        Tuple(e1,e2) --
            e1 = urllib response
            e2 = success or error code.

    Code Source: https://docs.python.org/3/howto/urllib2.html ('Fetching URLs')
    """
    if not validators.url(link):
        return ("", False, "Invalid link")
    print("Currently handling link: " + link)
    req = urllib.request.Request(link)
    try:
        response = urllib.request.urlopen(req)
    except HTTPError as error:
        return (None, False, error.code)
    except ContentTooShortError as error:
        return (None, False, "ContentTooShortError")
    except URLError as error:
        return (None, False, error.reason)
    else:
        return (response, True, "")



# Tests for functions in crawler.py
if __name__ == "__main__":
    print(crawl_link("https://a.com"))
