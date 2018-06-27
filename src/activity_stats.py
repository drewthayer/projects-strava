from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

#import StravaActivity
#from StravaActivity.py import StravaActivity
#from scripts.pymongo_scripts.py import docs_from_mongodb_collection

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
        self.tot_dist_m = self.dist[-1]
        self.tot_dist_mi = None
        self.tot_time_sec = self.time[-1]
        self.tot_time_hr = None
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

        self.slopes = np.array(self.slopes)

    def calc_velocities(self):
        ''' calculate velocities for each interval
        input:  self.dist (list)
                self.time (list)
        returns:
                self.velocities (np array)
        '''
        xx = self.dist + [self.dist[-1] + 0.1] # plus dx to avoid div/0
        tt = self.time + [self.time[-1] + 0.1]

        delta_x = np.diff(np.array(xx))
        delta_t = np.diff(np.array(tt))
        self.velocities = delta_x / delta_t
        self.max_velocity = np.max(self.velocities)


    def standard_units(self):
        ''' calculate standard units for easy interpretation'''
        conv_meter_mile = 1600
        # migrate numpy arrays up for derivative
        # distance
        self.tot_dist_mi = self.tot_dist_m / conv_meter_mile
        # time
        self.tot_time_hr = self.tot_time_sec / 60 / 60
        # velocity
        vel = np.array(self.velocities)
        self.mph = vel * 1/conv_meter_mile * 60 * 60

    def print_summary(self):
        print('\nactivity: {}'.format(self.name))
        print('distance: {:0.2f} mi'.format(self.tot_dist_mi))
        print('time: {:0.2f} hr'.format(self.tot_time_hr))
        print('average speed: {:0.2f} mph'.format(self.tot_dist_mi / self.tot_time_hr))
        print('max speed = {:0.2f} mph'.format(np.max(self.max_velocity)))


    def fit(self):
        ''' perform all calculations '''
        self.calc_slopes()
        self.calc_velocities()
        self.standard_units()
        self.print_summary()


    def calc_ascend_descend(self):
        delta = np.diff(self.elev)
        delta = np.append(delta, 0) # append 0 to match length
        # masks
        ascending = delta >= 0
        descending = delta < 0
        self.slopes_ascend = self.slopes[ascending]
        self.slopes_descend = self.slopes[descending]
        self.vel_ascend = self.velocities[ascending]
        self.vel_descend = self.velocities[descending]


    def ascend_descend_stats(self):
        print('mean ascending slope = {:0.3f}'.format(np.mean(self.slopes_ascend)))
        print('mean descending slope = {:0.3f}'.format(np.mean(self.slopes_descend)))
        print('\nmean ascending speed = {:0.2f} mph'.format(np.mean(self.vel_ascend)))
        print('mean descending speed = {:0.2f} mph'.format(np.mean(self.vel_descend)))


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

    # test: one activity
    act = StravaActivity(activities[0])
    act.fit()



    # switch:
    calc_stats = True
    # fit and plot all activities from class
    if calc_stats:
        for activity in activities:
           act = StravaActivity(activity)
           act.fit()
    else: print('plots off')
