# Database for Crawling -- Elvis
Using Mongodb and PyMongo for storing datas to local database

This database doesn't allow duplicate items, having URL as the key.
Scanner helps to check if any URL has expired or not and needs to be crawled again.
## Testing

As a prerequisite you should setup and install Mongodb and PyMongo

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/ - Mongodb
https://api.mongodb.com/python/current/installation.html - PyMongo

Create and run the database in cmd, default is
`C:\Program Files\MongoDB\Server\4.0\bin\mongod.exe" --dbpath="c:\data\db`

To run the code:
`python db.py` in cmd
