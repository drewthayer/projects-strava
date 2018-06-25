from stravalib.client import Client
from stravalib import unithelper
import os
import requests
from pymongo import MongoClient
import numpy as np

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

def write_activities_to_mongo(activities, types, collection):
    all_activities = [x for x in activities] # list of all activities for user
    i = 0
    for activity in all_activities:
        act_id = activity.id
        name = activity.name
        streams = client.get_activity_streams(activity.id, types=types, resolution='medium')

        # parse streams data
        latlng = np.array(streams['latlng'].data)
        ts = streams['time'].data
        alt = streams['altitude'].data
        dist = streams['distance'].data
        lat = latlng[:,0]
        lon = latlng[:,1]

        # insert activity to collection
        d = {}
        d['activity_' + str(act_id)] = {
                    'name': name,
                    'ts_id': streams['time'].data,
                    'altitude': streams['altitude'].data,
                    'distance': streams['distance'].data,
                    'lat': latlng[:,0].tolist(), # serialize np arrays
                    'lon': latlng[:,1].tolist()}

        collection.insert_one(d)
        i += 1

    print('{} activities written to mongodb'.format(i))

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

    # initiate mongo database, connect, make collection
    db_client = MongoClient('localhost',27017)  # Establish connection to persistent storage
    db = db_client.Strava  # Access/Initiate Database
    coll_name = '{}_{}_user'.format(athlete.firstname, athlete.lastname)
    collection = db[coll_name]

    # write activities to mongodb
    types = ['name', 'time', 'latlng', 'altitude', 'distance']
    write_activities_to_mongo(activities, types, collection)
