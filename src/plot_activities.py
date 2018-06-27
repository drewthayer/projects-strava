from pymongo import MongoClient
import matplotlib.pyplot as plt
import folium
import numpy as np

from StravaActivity import StravaActivity
from scripts.pymongo_scripts import docs_from_mongodb_collection

def plot_all(activities_list, switch=True):
    if switch:
        for activity in activities_list:
           act = StravaActivity(activity)
           act.fit()
           act.plot_all()
    else: print('\nplots: off')

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
    latlon_all = []
    for activity in activities:
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

    #
    # # plot slopes, together
    # for idx, vec in enumerate(slopes):
    #     plt.plot(d['distance'], vec, markersize=2)
    # plt.xlabel('distance (m)')
    # plt.ylabel('slope')
    # plt.title('slopes')
    # plt.show()
    #plt.savefig('../figs/slope_profiles/{}_slope.png'.format(names[idx]), dpi=250)
    #plt.close()
