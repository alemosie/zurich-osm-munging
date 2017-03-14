from pymongo import MongoClient
import json

"""
Insert sanitized OSM data in JSON format into MongoDB
"""

def insert_data(filename, db):
    # first: to connect to the db/shell:
        # => mongod --dbpath ~/mongodb/data/db/
        # => mongo
        # => help
        # => use <name of db> to either switch to or create db
    with open(filename) as json_file:
        data = json.loads(json_file.read())
        db.just_zurich.insert_many(data)
        print db.just_zurich.find_one()

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.osm
    insert_data('data/just_zurich.json', db)
