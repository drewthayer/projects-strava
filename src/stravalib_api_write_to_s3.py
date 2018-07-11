from stravalib.client import Client
from stravalib import unithelper
import os
import requests
from pymongo import MongoClient
import numpy as np
import boto3
import json


def get_athlete(client):
    athlete = client.get_athlete()
    print('athlete id: {}, name: {} {}'.format(athlete.id,
        athlete.firstname, athlete.lastname))
    return athlete

def get_activities(client,limit):
    #Returns a list of Strava activity objects, up to the number specified by limit
    activities = client.get_activities(limit=limit)
    assert len(list(activities)) == limit
    for item in activities:
        print(item)
    return activities

def create_s3_bucket(bucketname):
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucketname)

def write_to_s3(bucket, data, fname):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket,fname)
    obj.put(Body=json.dumps(data))


def write_activities_to_s3(activities, types, bucket):
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

        # dictionary of activity
        d = {}
        dname = 'activity_' + str(act_id)
        d[dname] = {
                    'name': name,
                    'ts_id': streams['time'].data,
                    'altitude': streams['altitude'].data,
                    'distance': streams['distance'].data,
                    'lat': latlng[:,0].tolist(), # serialize np arrays
                    'lon': latlng[:,1].tolist()}

        #write dictionary to s3 as json
        write_to_s3(bucket, d, dname + '.json')

        i += 1

    print('{} activities written to s3'.format(i))
    return out

if __name__=='__main__':
    # id and port info
    client_id = open('client.id')
    client_secret = os.environ['STRAVA_CLIENT_SECRET']
    access_token = os.environ['STRAVA_ACCESS_TOKEN']
    port = 5000
    url = 'http://localhost:%d/authorized' % port

    # initialize stravalib client
    client = Client()
    authorize_url = client.authorization_url(client_id=client_id, redirect_uri=url)

    # get strava athlete
    client.access_token = access_token
    athlete = get_athlete(client)

    # get activities for athlete
    activities = get_activities(client, limit=30)

    # features to save
    types = ['name', 'time', 'latlng', 'altitude', 'distance']

    # write to s3
    bucket = 'strava-project'
    create_s3_bucket(bucket)
    write_activities_to_s3(activities, types, bucket)
