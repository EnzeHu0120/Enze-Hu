import json
from pymongo import MongoClient
from random import randint


def create_db(client,tf_idf,important_tags):
        db=client.CS121Project3
        for term in tf_idf:
                db.TfIdf.insert(json.loads(json.dumps({'term':term,'URLs':tf_idf[term]})), check_keys=False)

        for url in important_tags:
                db.Tags.insert(json.loads(json.dumps({'URL':url, "tags": important_tags[url]})), check_keys=False)
