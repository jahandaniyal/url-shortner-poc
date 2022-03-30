import os
import itertools
import string
import random
from pymongo import MongoClient


# def get_db():
#     client = MongoClient(host='localhost',
#                          port=27017,
#                          username='root',
#                          password='pass',
#                         authSource="admin")
#     db = client["animal_db"]
#     return db

#

def get_db_client():
    # client = MongoClient(host='localhost',
    #                      port=27017,
    #                      username='root',
    #                      password='pass',
    #                     authSource="admin")

    client = MongoClient(host=os.environ.get('MONGO_HOST'),
                         port=27017,
                         username=os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
                         password=os.environ.get('MONGO_INITDB_ROOT_PASSWORD'),
                        authSource="admin")
    return client


def insert_data():
    client = get_db_client()
    db = client.url_db
    var1 = string.ascii_letters
    combs = list(itertools.permutations(list(var1), 3))
    print(len(combs))
    keys = []
    for item in combs:
        keys.append({'url': '', 'created_at': '', 'id': ''.join(item)})
    random.shuffle(keys)
    db.url_tb.drop()
    db.url_tb.insert_many(keys)
    db.url_tb.create_index('id')
    print("Database populated with keys: {}".format(db.url_tb.count_documents({})))
    return "Database populated with keys: {}".format(db.url_tb.count_documents({}))


if __name__ == '__main__':
    insert_data()