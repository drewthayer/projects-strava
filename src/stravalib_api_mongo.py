from stravalib.client import Client
from stravalib import unithelper
import os
import requests
from pymongo import MongoClient
import numpy as np

def insert_to_mongo(db, table, item):
    db.table.insert(item)
    print('inserted in db')

def get_activities(client,limit):
    #Returns a list of Strava activity objects, up to the number specified by limit
    activities = client.get_activities(limit=limit)
    assert len(list(activities)) == limit
    for item in activities:
        print(item)
    return activities

def get_athlete(client):
    athlete = client.get_athlete()
    print('athlete id: {}, name: {} {}'.format(athlete.id,
        athlete.firstname, athlete.lastname))
    return athlete

# id and port info
client_id = open('client.id')
client_secret = os.environ['STRAVA_CLIENT_SECRET']
access_token = os.environ['STRAVA_ACCESS_TOKEN']
port = 5000
url = 'http://localhost:%d/authorized' % port

if __name__=='__main__':
    # initialize stravalib client
    client = Client()
    authorize_url = client.authorization_url(client_id=client_id, redirect_uri=url)

    # get athlete
    client.access_token = access_token
    athlete = get_athlete(client)

    # get activities for athlete
    activities = get_activities(client, limit=10)

    # get one activity and access streams
    all_acts = [x for x in activities]
    act = all_acts[2]
    types = ['time', 'latlng', 'altitude', 'distance']
    streams = client.get_activity_streams(act.id, types=types, resolution='medium')

    # parse streams data
    latlng = np.array(streams['latlng'].data)
    ts = streams['time'].data
    alt = streams['altitude'].data
    dist = streams['distance'].data
    lat = latlng[:,0]
    lon = latlng[:,1]

    # initiate mongo database
    tableid = str(act.id)
    client = MongoClient('localhost:27017')  # Establish connection to persistent storage
    db = client.Strava  # Access/Initiate Database
    collection = db.activity1 # initiate collection
    #activity_table = db[tableid]        # Access/Initiate Table

    # insert activity to collection
    activity = {'ts_id': streams['time'].data,
                'altitude': streams['altitude'].data,
                'distance': streams['distance'].data,
                'lat': latlng[:,0].tolist(), # serialize np arrays
                'lon': latlng[:,1].tolist()}

    db.activity1.insert_one(activity)


    # # example: distances
    # dists= []
    # for act in activities:
    #     dists.append(act.distance) # list of distance objects
    #     print(unithelper.miles(act.distance)) # can call float() to get just number
    #
    #
    # # Activities can have many streams, you can request n desired stream types

    #
    # #  Result is a dictionary object.  The dict's key are the stream type.
    # if 'altitude' in streams.keys():
    #     print(streams['altitude'].data)
    #
    # # plot altitudes from a ride
    # import matplotlib.pyplot as plt
    # plt.plot(streams['altitude'].data)
    # plt.show()
    #
    # if 'latlng' in streams.keys(): # this works, plot in folium
    #     print('yes')
    #
    # # plot lat long with matplotlib
    # # loop method
    # latlng = streams['latlng'].data # list of lists
    # fig, ax = plt.subplots()
    # for pair in latlng:
    #     plt.plot(pair[0], pair[1], 'ok')
    # plt.show()
    #
    # # numpy method way faster
    # import numpy as np
    # latlng = np.array(streams['latlng'].data)
    # plt.plot(lon, lat, 'ok')
    # plt.axis('equal')
    # plt.show()
