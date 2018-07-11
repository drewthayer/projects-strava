def activities_to_json(activities, types):
    all_activities = [x for x in activities] # list of all activities for user
    i = 0
    out = []
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
        dname = 'activity_' + str(act_id)
        d[dname] = {
                    'name': name,
                    'ts_id': streams['time'].data,
                    'altitude': streams['altitude'].data,
                    'distance': streams['distance'].data,
                    'lat': latlng[:,0].tolist(), # serialize np arrays
                    'lon': latlng[:,1].tolist()}
        out.append(d)
        #collection.insert_one(d)
        i += 1

    print('{} activities written'.format(i))
    return out
