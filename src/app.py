"""This is the server module.

This starts up the restful web service that will direct
requests to specific components.

"""

import ast
from flask import Flask
from flask_restful import Api, Resource, reqparse
from crawl.scheduler import Scheduler

APP = Flask(__name__)
API = Api(APP)

class DomainCrawl(Resource):
    """The crawl API endpoint process URLs

    Available methods:
        - POST
    """

    @staticmethod
    def post():
        """The POST endpoint that crawls & processes links

        Payload:
            [JSON] -- JSON Object containing a URLS key that contains a list of URLs

        Returns:
            [JSON] -- JSON Object containing a list of bad URLs
        """
        parser = reqparse.RequestParser()
        parser.add_argument("URLS")
        args = parser.parse_args()
        if args["URLS"] is None:
            return "Bad Request: No URLS key found", 500
        urls = ast.literal_eval(args["URLS"])
        payload = []
        for url in urls:
            payload.append(urls[url])
        SCHEDULER.dump_hp_links(payload) # Send the URLs to the scheduler
        SCHEDULER.print_crawled_hp()
        return "Success", 200

API.add_resource(DomainCrawl, "/crawl")

# Start the scheduler thread
SCHEDULER = Scheduler(5)
SCHEDULER.start()

# Start the server
APP.run(debug=True)
