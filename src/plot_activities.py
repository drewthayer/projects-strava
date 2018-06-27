from pymongo import MongoClient
import matplotlib.pyplot as plt
import folium
import numpy as np

import StravaActivity

def docs_from_mongodb_collection(db, coll_name):
    coll = db[coll_name]
    docs = []
    for doc in coll.find():
        docs.append(doc)
    return docs



if __name__=='__main__':
    # initiate mongo database and connect
    client = MongoClient('localhost',27017)  # Establish connection to persistent storage
    db = client.Strava  # Access/Initiate Database
    acts_list = docs_from_mongodb_collection(db,'Drew_Thayer_user') # list of activities, with id

    # list of activities
    activities = [list(item.values())[1] for item in acts_list]

    # switch:
    make_plots = True
    # fit and plot all activities from class
    if make_plots:
        for activity in activities:
           act = StravaActivity(activity)
           act.fit()
           act.plot_all()
    else: print('plots off')

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
