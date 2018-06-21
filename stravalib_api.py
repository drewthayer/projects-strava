from stravalib.client import Client
import os
import requests

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
port = 5000
url = 'http://localhost:%d/authorized' % port

if __name__=='__main__':
    client = Client()
    authorize_url = client.authorization_url(client_id=client_id, redirect_uri=url)
    # Have the user click the authorization URL, a 'code' param will be added to the redirect_uri
    # .....

    access_token = os.environ['STRAVA_ACCESS_TOKEN']

    client.access_token = access_token
    get_athlete(client)

    athlete = client.get_athlete()
    activities = get_activities(client, limit=10)
