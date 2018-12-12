""" This contains the functions for parsing robots.txt pages.

    The get_bad_paths function should be used to get the paths which
    are disallowed from the robots.txt page at a given URL.

    Tests can be found in the appropriate file.
"""

import sys
sys.path.append("../")

from crawl import crawler


def get_bad_paths(link):
    """ Reads a robots.txt file, given its URL, and returns a list of
        paths which are not allowed to be crawled.

        Input:
            link -- the URL of a robots.txt file

        Output:
            A list of paths to files that are disallowed by the
            robots.txt file.
    """
    response = crawler.crawl_link(link)
    if response[1]:
        return parse(response[0].read().decode("unicode_escape"))
    return []


def parse(text):
    """ Parses a robots.txt page, given the page's contents as a string,
        and returns a list of paths which are not allowed to be crawled.

        Input:
            text -- the contents of a robots.txt file

        Output:
            A list of paths to files that are disallowed by the
            robots.txt file.
    """
    # blocked_paths is the list of websites to be blocked.
    blocked_paths = []
    # blocks_apply is True if the current lines apply to our crawler.
    blocks_apply = True

    lines = text.split("\n")

    for line in lines:
        orig_line = line
        # Ignore comments and blank lines
        line = line.strip()

        if line.startswith("#") or line == "":
            continue

        # Remove any comments that take up part of a line
        line_parts = line.split("#")
        line = line_parts[0].lower()

        # Check if the user-agent applies.
        if line.startswith("user-agent:"):
            parts = line.split(":", 1)
            agent = parts[1].strip()
            blocks_apply = agent == "*"
        # Record what pages the crawler is not allowed to crawl.
        elif line.startswith("disallow:"):
            if blocks_apply:
                parts = line.split(":", 1)
                path = parts[1].strip()
                blocked_paths.append(path)
        # There's no good way to handle specifically allowed paths.
        elif line.startswith("allow:"):
            continue
        else:
            print("Could not parse line:", orig_line)

    return blocked_paths
