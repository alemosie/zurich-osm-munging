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
        db.just_zurich.insert_many(data)
        print db.just_zurich.find_one()

# number of chosen type of nodes, like cafes, shops etc.

def print_pipeline():
    filter_nulls = {"$match": {"name": {"$exists": 1}}}
    group_names = {"$group": {
                        "_id": "$name",
                        "count": {"$sum": 1}
                    }
                }
    sort = {"$sort": {"count": -1}}
    limit = {"$limit": 1}
    pipeline = [filter_nulls, group_names, sort, limit]


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.osm
    insert_data('data/just_zurich.json', db)

# > db.zurich.count()
# 6084959
# > db.zurich.distinct("created.user").length
# 2644
