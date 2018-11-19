"""This is the server module.

This starts up the restful web service that will direct
requests to specific components.

"""

import ast
import validators
from datetime import datetime, timedelta
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from crawl.scheduler import Scheduler
from parser.parser import get_bad_paths
from database.db import insertion, connect_db

APP = Flask(__name__)
API = Api(APP)
SCHEDULER = Scheduler(5)
collection = connect_db()


class RobotsCrawl(Resource):
    """The robots.txt API endpoint to retreive what links not to crawl

    Available methods:
        - GET
    """

    @staticmethod
    def get():
        domain = request.args.get('url')
        if (domain == None or not validators.url(domain)):
            return "Bad Request: Bad URL Sent", 400
        else:
            return get_bad_paths(domain), 200

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
        # Ensure payload is valid
        if args["URLS"] is None:
            return "Bad Request: No URLS key found", 400

        # Parse the payload
        urls = ast.literal_eval(args["URLS"])
        payload = []
        for url in urls:
            payload.append(urls[url])

        # Send the URLs to the scheduler
        results = SCHEDULER.dump_hp_links(payload)

        return_obj = [] # Return object to the request
        html_payload = [] # Payload containing the HTML texts
        for result in results.keys():
            if results[result][1] is True:
                html_payload.append([result, results[result][0].read()])
                insertion(collection, result, 7, datetime.now(), True)
            else:
                return_obj.append(result)
                insertion(collection, result, 7, datetime.now(), False)

        ### Implement the API request to text transformation & Indexing

        return return_obj, 200


def main():
    """Run the web server
    """

    API.add_resource(DomainCrawl, "/crawl")
    API.add_resource(RobotsCrawl, '/robots')

    # Start the DB
    # Start the scheduler thread
    SCHEDULER.start()

    # Start the server
    APP.run(port=80, host='0.0.0.0')

if __name__ == '__main__':
    main()
