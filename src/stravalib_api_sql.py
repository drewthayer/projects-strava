from stravalib.client import Client
from stravalib import unithelper
import os
import requests
from sqlite3_scripts import connect_to_sql, create_table_sql

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

# id and port info
client_id = open('client.id')
client_secret = os.environ['STRAVA_CLIENT_SECRET']
access_token = os.environ['STRAVA_ACCESS_TOKEN']
port = 5000
url = 'http://localhost:%d/authorized' % port

if __name__=='__main__':
    # initiate mongo database
    #client = MongoClient()        # Establish connection to persistent storage
    #db = client['Strava']  # Access/Initiate Database
    #activity_table = db['activities']        # Access/Initiate Table

    # initialize stravalib client with url, access token
    client = Client()
    authorize_url = client.authorization_url(client_id=client_id, redirect_uri=url)

    client.access_token = access_token
    get_athlete(client)

    athlete = client.get_athlete()
    activities = get_activities(client, limit=10)

    streams = client.get_activity_streams(act.id, types=types, resolution='medium')
    #  Result is a dictionary object.  The dict's key are the stream type.
    if 'altitude' in streams.keys():
        print(streams['altitude'].data)

    # example: get distances
    dists= []
    for act in activities:
        dists.append(act.distance) # list of distance objects
        print(unithelper.miles(act.distance)) # can call float() to get just number

    # get types from Activities
    all_acts = [x for x in activities]
    act = all_acts[2]
    # Activities can have many streams, you can request n desired stream types
    types = ['time', 'latlng', 'altitude', 'heartrate', 'temp', ]


    # write streams to sql db
    # make new table
    conn = connect_to_sql('../db/strava_data.db')
    table_id = str(act.id)
    sql = ''' CREATE TABLE IF NOT EXISTS table_id (
        ts_id integer PRIMARY KEY,
        altitude integer NOT NULL,
        distance integer NOT NULL,
        lat integer NOT NULL,
        lon integer NOT NULL);'''
    create_table_sql(conn, 'ride1', sql)

    # parse lat, lon data
    latlng = np.array(streams['latlng'].data)
    ts = streams['time'].data
    alt = streams['altitude'].data
    dist = streams['distance'].data
    lat = latlng[:,0]
    lon = latlng[:,1]

    # insert data to table
    sql = '''INSERT INTO table_id (
        ts_id, altitude, distance, lat, lon)
        VALUES
            (ts,
            alt,
            dist,
            lat,
            lon); '''

    cursor = conn.cursor()
    cursor.execute(sql)


    # plot altitudes from a ride
    import matplotlib.pyplot as plt
    plt.plot(streams['altitude'].data)
    plt.show()

    if 'latlng' in streams.keys(): # this works, plot in folium
        print('yes')

    # plot lat long with matplotlib
    # loop method
    latlng = streams['latlng'].data # list of lists
    fig, ax = plt.subplots()
    for pair in latlng:
        plt.plot(pair[0], pair[1], 'ok')
    plt.show()

    # numpy method way faster
    import numpy as np
    latlng = np.array(streams['latlng'].data)
    plt.plot(latlng[:,1], latlng[:,0], 'ok')
    plt.axis('equal')
    plt.show()
