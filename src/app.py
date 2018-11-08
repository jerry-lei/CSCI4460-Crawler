from flask import Flask
from flask_restful import Api, Resource, reqparse
from crawl.scheduler import Scheduler
import time
import ast

app = Flask(__name__)
api = Api(app)

class DomainCrawl(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("URLS")
        args = parser.parse_args()
        if args["URLS"] == None:
            return "Bad Request: No URLS key found", 500
        urls = ast.literal_eval(args["URLS"])
        payload = []
        for url in urls:
            payload.append(urls[url])
        scheduler.dump_hp_links(payload)
        scheduler.print_crawled_hp()
        return "Success", 200

api.add_resource(DomainCrawl, "/crawl")

# Start the scheduler thread
scheduler = Scheduler(5)
scheduler.start()

# Start the server
app.run(debug=True)
