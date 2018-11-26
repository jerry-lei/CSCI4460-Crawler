"""This is the server module.

This starts up the restful web service that will direct
requests to specific components.

"""

import ast
import validators
import requests
from datetime import datetime, timedelta
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from crawl.scheduler import Scheduler
from parser.parser import get_bad_paths
from database.db import insertion, connect_db
from database.scanner import db_scanner
from threading import Timer

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

        return_obj = send_requests(results)
        return return_obj, 200

def send_requests(results):
    """Handles building out the payloads and sending each payload to the other components

    Arguments:
        results {Dictionary} -- Map containing successfully & unsuccessfully crawled links

    Returns:
        [List] - List of failed links
    """

    return_obj = [] # Return object to the request
    html_payload = [] # Payload containing the HTML texts
    for result in results.keys():
        if results[result][1] is True:
            html_payload.append([result, results[result][0].read()])
            insertion(collection, result, 7, datetime.now(), True)
        else:
            return_obj.append(result)
            insertion(collection, result, 7, datetime.now(), False)
    req_tt = requests.post('TT_URL', data=html_payload)
    req_index = requests.post('INDEX_URL', data=return_obj)
    return return_obj


def handle_db_scanner():
    """The callback function to handle scanning the database for expired links
    """

    links = db_scanner(collection)
    results = SCHEDULER.dump_lp_links(links)
    send_requests(results)
    t = Timer(86400, handle_db_scanner) # Run the thread once every day
    t.start()

def main():
    """Run the web server
    """

    API.add_resource(DomainCrawl, "/crawl")
    API.add_resource(RobotsCrawl, '/robots')

    # Start the scheduler thread
    SCHEDULER.start()

    # Start the DB Scanner thread
    t = Timer(0, handle_db_scanner)
    t.start()

    # Start the server
    APP.run(port=3000, host='0.0.0.0')

if __name__ == '__main__':
    main()
