from pymongo import MongoClient
import matplotlib.pyplot as plt
import folium
import numpy as np

def docs_from_mongodb_collection(db, coll_name):
    coll = db[coll_name]
    docs = []
    for doc in coll.find():
        docs.append(doc)
    return docs

class StravaActivity(object):
    ''' a class for attributes of a Strava activity '''

    def __init__(self, d):
        self.name = d['name']
        self.type = None
        self.dist = d['distance']
        self.time = d['ts_id']
        self.elev = d['altitude']
        self.lat = d['lat']
        self.lon = d['lon']
        self.tot_distance = self.dist[-1]
        self.tot_time = self.time[-1]
        self.start_elev = self.elev[0]
        self.slopes = []
        self.velocities = []
        self.mph = []

    def calc_slopes(self):
        ''' calculate slopes for each interval'''
        # pad the end with ~ last val
        xx = self.dist + [self.dist[-1] + 0.1] # plus dx to avoid div/0
        yy = self.elev + [self.elev[-1]]
        for idx in range(len(xx) - 1):
            self.slopes.append((yy[idx + 1] - yy[idx])/(xx[idx + 1] - xx[idx]))

    def calc_velocities(self):
        ''' calculate velocities for each interval'''
        xx = self.dist + [self.dist[-1] + 0.1] # plus dx to avoid div/0
        tt = self.time + [self.time[-1] + 0.1]
        for idx in range(len(xx) - 1):
            self.velocities.append((xx[idx + 1] - xx[idx])/(tt[idx + 1] - tt[idx]))

    def standard_units(self):
        ''' calculate standard units for easy interpretation'''
        meter_mile_conv = 1600
        # migrate numpy arrays up for derivative
        vel = np.array(self.velocities)
        self.mph = vel * 1/meter_mile_conv * 60 * 60

    def fit(self):
        ''' perform all calculations '''
        self.calc_slopes()
        self.calc_velocities()
        self.standard_units()

    def plot_xy(self):
        plt.plot(self.lon, self.lat, 'ok')
        plt.axis('equal')
        plt.xlabel('longitude')
        plt.ylabel('latitude')
        plt.title(self.name + ' map')
        plt.savefig('../figs/xy/{}_xy.png'.format(self.name), dpi=250)
        plt.close()

    def plot_map_folium(self):
        m = folium.Map(location=[self.lat, self.lon],
              tiles='OpenStreetMap')
        return m

    def plot_elev_profiles(self):
        plt.plot(self.dist, self.elev, 'ok', markersize=2)
        plt.xlabel('distance (m)')
        plt.ylabel('elevation (m)')
        plt.title(self.name + ' elevation profile')
        #plt.axis('equal')
        #plt.show()
        plt.savefig('../figs/elev_profiles/{}_elev.png'.format(self.name), dpi=250)
        plt.close()

    def plot_slopes(self):
        plt.plot(self.dist, self.slopes, 'og', markersize=2)
        plt.xlabel('distance (m)')
        plt.ylabel('slope')
        plt.title(self.name + ' slope')
        plt.savefig('../figs/slope_profiles/{}_slope.png'.format(self.name), dpi=250)
        plt.close()

    def plot_mph(self):
        plt.plot(self.dist, self.mph, 'ob', markersize=2)
        plt.xlabel('distance (m)')
        plt.ylabel('mph')
        plt.title(self.name + ' speed')
        plt.savefig('../figs/speed/{}_speed.png'.format(self.name), dpi=250)
        plt.close()

    def plot_all(self):
        ''' generate all plots '''
        self.plot_xy()
        self.plot_elev_profiles()
        self.plot_slopes()
        self.plot_mph()

if __name__=='__main__':
    # initiate mongo database and connect
    client = MongoClient('localhost',27017)  # Establish connection to persistent storage
    db = client.Strava  # Access/Initiate Database
    acts_list = docs_from_mongodb_collection(db,'Drew_Thayer_user') # list of activities, with id

    # list of activities
    activities = [list(item.values())[1] for item in acts_list]

    # names (update)
    names = ['Horsetooth ride', 'Butler Gulch ski', 'Lookout ride', 'ride4', 'Torreys Peak ski', 'ride6',
            'Glassier Buckthorn ride', 'Hay Park ride', 'Carbondale ride', 'ride10',]

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
