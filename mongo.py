from pymongo import MongoClient
import json


def insert_data(filename, db):
    # to connect to the shell:
        # => mongod --dbpath ~/mongodb/data/db/
        # => mongo
        # => help
        # => use <name of db> to either switch to or create db

    with open(filename) as json_file:
        data = json.loads(json_file.read())
        db.zurich.insert_many(data)
        print db.zurich.find_one()

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.osm
    insert_data('zurich.json')

# > db.zurich.count()
# 6084959
# > db.zurich.distinct("created.user").length
# 2644
