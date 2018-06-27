from pymongo import MongoClient

def docs_from_mongodb_collection(db, coll_name):
    coll = db[coll_name]
    docs = []
    for doc in coll.find():
        docs.append(doc)
    return docs
