from pymongo import MongoClient

def dict_from_mongodb_collection(db,coll_name):
    coll = db[coll_name]
    d = list(coll.find())[0]
    return d

def docs_from_mongodb_collection(db,coll_name):
    coll = db[coll_name]
    docs = []
    for doc in coll.find():
        docs.append(doc)
    return docs

if __name__=='__main__':
    # initiate mongo database and connect
    client = MongoClient('localhost',27017)  # Establish connection to persistent storage
    db = client.Strava  # Access/Initiate Database
    #d = dict_from_mongodb_collection(db,'Drew_Thayer') # dict of docs in collection
    l = docs_from_mongodb_collection(db,'Drew_Thayer') # list of activities, with id

    # list of activities
    activities = []
    for item in l:
        activities.append(list(item.values())[1])



    # print "All entries:"
    # print list(coll.find())
    # print

    # plot all rides xy
    import matplotlib.pyplot as plt
    for d in activities:
        plt.plot(d['lon'], d['lat'], 'ok')
        plt.axis('equal')
        plt.show()
