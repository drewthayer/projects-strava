from pymongo import MongoClient
import matplotlib.pyplot as plt

from StravaActivity import StravaActivity
from scripts.pymongo_scripts import docs_from_mongodb_collection

def plot_all(activities_list, switch=True):
    ''' run plot scripts in StravaActivity class '''
    if switch:
        for activity in activities_list:
           act = StravaActivity(activity)
           act.fit()
           act.plot_all()
    else: print('\nplots: off')

def plot_all_xy_one_map(activities_list, switch):
    '''
    plots all activities on same XY map
    requires StravaActivity class '''
    if switch:
        latlon_all = []
        for activity in activities_list:
           act = StravaActivity(activity)
           act.fit()
           lat = act.lat
           lon = act.lon
           latlon_all.append((lat,lon))

        for latlon in latlon_all:
            plt.plot(latlon[1], latlon[0], 'o', markersize=2)
        plt.xlabel('lon')
        plt.ylabel('lat')
        plt.show()

if __name__=='__main__':
    # initiate mongo database and connect
    client = MongoClient('localhost',27017)  # Establish connection to persistent storage
    db = client.Strava  # Access/Initiate Database
    acts_list = docs_from_mongodb_collection(db,'Drew_Thayer_user') # list of activities, with id

    # list of activities
    activities = [list(item.values())[1] for item in acts_list]

    # fit and plot all activities from class
    plot_all(activities, switch=True)

    # plot all activities in map together
    plot_all_xy_one_map(activities, switch=True)
