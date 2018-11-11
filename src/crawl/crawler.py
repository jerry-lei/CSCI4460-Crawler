""" This script the function to crawl links.


Good test cases & their behaviors:

https://.com -- crawl_link returns an error -- none of the excepts catch this
https://rpi.edu.com -- takes a long time to respond

"""


import urllib.request
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
    print("Currently handling link: " + link)
    my_link = link
    req = urllib.request.Request(my_link)
    try:
        response = urllib.request.urlopen(req)
    except HTTPError as error:
        return (None, error.code)
    except URLError as error:
        return (None, error.reason)
    except ContentTooShortError as error:
        return (None, "ContentTooShortError")
    else:
        return (response, "Success")



# Tests for functions in crawler.py
if __name__ == "__main__":
    print(crawl_link("https://a.com"))
