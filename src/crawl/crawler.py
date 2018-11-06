import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError

""" Source: https://docs.python.org/3/howto/urllib2.html ('Fetching URLs')
"""
def crawl_link(link):
    print("Currently handling link: " + link)
    my_link = link
    req = urllib.request.Request(my_link)
    try:
        response = urllib.request.urlopen(req)
    except HTTPError as e:
        return (None, e.code)
    except URLError as e:
        return (None, e.reason)
    except ContentTooShortError as e:
        return (None, "ContentTooShortError")
    else:
        return (response, "Success")


""" GOOD TEST CASES:
https://.com <--- returns an error (not caught by try/catch)
https://rpi.edu.com <--- takes very long to return error
"""



# Tests for functions in crawler.py
if __name__ == "__main__":
    print(crawl_link("https://a.com"))
