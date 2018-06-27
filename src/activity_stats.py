from pymongo import MongoClient

from scripts.StravaActivity import StravaActivity
from scripts.pymongo_scripts import docs_from_mongodb_collection

def fit_all(activities_list, switch=True):
    if switch:
        for activity in activities_list:
           act = StravaActivity(activity)
           act.fit()
    else: print('\nstats for all activities: off')

if __name__=='__main__':
    # initiate mongo database and connect
    client = MongoClient('localhost',27017)  # Establish connection to persistent storage
    db = client.Strava  # Access/Initiate Database
    acts_list = docs_from_mongodb_collection(db,'Drew_Thayer_user') # list of activities, with id

    # list of activities
    activities = [list(item.values())[1] for item in acts_list]

    # test: one activity
    act = StravaActivity(activities[0])
    act.fit()

    # fit and plot all activities from class
    fit_all(activities, switch=True)
