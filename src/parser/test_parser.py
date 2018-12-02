import parser

if __name__ == '__main__':
    print("my part:", get_bad_paths("http://rpi.edu/robots.txt"))
    print("my part:", get_bad_paths("http://cs.rpi.edu/robots.txt"))
    print("my part:", get_bad_paths("http://rpi.edu/robots.taxt"))
    print("my part:", get_bad_paths("https://www.google.com/search?q=null?"))
    print("my part:", get_bad_paths("https://en.wikipedia.org/robots.txt"))
    print("my part:", get_bad_paths("https://www.pgdp.net/robots.txt"))
    print("my part:", get_bad_paths("http://homepages.rpi.edu/~tullyw/test_robots.txt"))


