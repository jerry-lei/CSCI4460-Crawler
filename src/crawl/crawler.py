import urllib.request

""" Source: https://docs.python.org/3/howto/urllib2.html ('Fetching URLs')
"""
def crawl_link(link):
    my_link = link
    html = None
    with urllib.request.urlopen(my_link) as response:
        html = response.read()
    return html


# Tests for functions in crawler.py
if __name__ == "__main__":
    print(crawl_link("https://google.com"))
