from pymongo import MongoClient
import matplotlib.pyplot as plt
import folium

def dict_from_mongodb_collection(db, coll_name):
    coll = db[coll_name]
    d = list(coll.find())[0]
    return d

def docs_from_mongodb_collection(db, coll_name):
    coll = db[coll_name]
    docs = []
    for doc in coll.find():
        docs.append(doc)
    return docs

class StravaActivity(object):
    ''' a class for attributes of a Strava activity '''

    def __init__(self, name):
        self.name = name
        self.type = None
        


if __name__=='__main__':
    # initiate mongo database and connect
    client = MongoClient('localhost',27017)  # Establish connection to persistent storage
    db = client.Strava  # Access/Initiate Database
    acts_list = docs_from_mongodb_collection(db,'Drew_Thayer') # list of activities, with id

    # list of activities
    activities = [list(item.values())[1] for item in acts_list]

    # names (update)
    names = ['ride1', 'ride2', 'ride3', 'ride4', 'ride5', 'ride6',
            'ride7', 'ride8', 'ride9', 'ride10',]


    # plot all rides xy
    # for d in activities:
    #     plt.plot(d['lon'], d['lat'], 'ok')
    #     plt.axis('equal')
    #     plt.show()

    # folium mpas
    act = activities[0]
    m = folium.Map(location=[act['lon'], act['lat']],
              tiles='OpenStreetMap')

    # plot elevation profiles
    for idx, d in enumerate(activities):
        plt.plot(d['distance'], d['altitude'], 'ok', markersize=2)
        plt.xlabel('distance (m)')
        plt.ylabel('elevation (m)')
        plt.title(names[idx])
        #plt.axis('equal')
        #plt.show()
        plt.savefig('../figs/elev_profiles/{}_elev.png'.format(names[idx]), dpi=250)
        plt.close()

    # grade analysis
    # calculate slopes for each ride
    slopes = []
    for d in activities:
        slope_vec = []
        xx = d['distance'] + [d['distance'][-1] + 0.1]
        yy = d['altitude'] + [d['altitude'][-1]]
        for idx in range(len(xx) - 1):
            slope_vec.append((yy[idx + 1] - yy[idx])/(xx[idx + 1] - xx[idx]))
        slopes.append(slope_vec)

    # plot slopes, separate
    for idx, vec in enumerate(slopes):
        plt.plot(d['distance'], vec, 'og', markersize=2)
        plt.xlabel('distance (m)')
        plt.ylabel('slope')
        plt.title(names[idx] + ' slope')
        plt.savefig('../figs/slope_profiles/{}_slope.png'.format(names[idx]), dpi=250)
        plt.close()

    # plot slopes, together
    for idx, vec in enumerate(slopes):
        plt.plot(d['distance'], vec, markersize=2)
    plt.xlabel('distance (m)')
    plt.ylabel('slope')
    plt.title('slopes')
    plt.show()
    #plt.savefig('../figs/slope_profiles/{}_slope.png'.format(names[idx]), dpi=250)
    #plt.close()
