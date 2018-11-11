
import sys
sys.path.append("../")

from crawl import crawler





def get_bad_paths(link):

	(response, status) = crawler.crawl_link(link)

	if status == "Success":
		return parse(response.read().decode())
	else:
		return []


def parse(text):
	allowed_paths = []
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
		line = line_parts[0]

		# Check if the user-agent applies.
		if line.lower().startswith("user-agent:"):
			parts = line.split(":", 1)
			agent = parts[1].strip()
			if (agent == "*"):
				blocks_apply = True
			else:
				blocks_apply = False

		# Record what pages the crawler is not allowed to crawl.
		elif line.lower().startswith("disallow:"):
			if blocks_apply:
				parts = line.split(":", 1)
				path = parts[1].strip()
				blocked_paths.append(path)
		else:
			print("Could not parse line:", orig_line)

	return blocked_paths


if __name__ == '__main__':
	print("my part:", get_bad_paths("http://rpi.edu/robots.txt"))
	print("my part:", get_bad_paths("http://cs.rpi.edu/robots.txt"))
	print("my part:", get_bad_paths("http://rpi.edu/robots.taxt"))
	print("my part:", get_bad_paths("https://www.google.com/search?q=null?"))
	print("my part:", get_bad_paths("https://en.wikipedia.org/robots.txt"))



