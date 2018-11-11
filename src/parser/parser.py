
import sys
sys.path.append("../")

from crawl import crawler





def important_stuff(link):

	(response, status) = crawler.crawl_link(link)

	if status == "Success":
		return parse(response.read())
	else:
		return []


def parse(text):
	return "Success!"


if __name__ == '__main__':
	print("my part:", important_stuff("http://rpi.edu/robots.txt"))
	print("my part:", important_stuff("http://rpi.edu/robots.taxt"))


