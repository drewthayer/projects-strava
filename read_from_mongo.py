from pymongo import MongoClient

if __name__=='__main__':
    # initiate mongo database and connect
    client = MongoClient('localhost',27017)  # Establish connection to persistent storage
    db = client.Strava  # Access/Initiate Database
