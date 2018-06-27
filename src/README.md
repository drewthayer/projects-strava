src folder README

### Workflow

1. get data from Strava api, save to mongo database
  - _read_from_mongo.py_: read strava user data, write to db

2. generate basic plots for activities
  - _plot_activities.py_

3. calculate basic ride statistics
  - _activity_stats.py_

4. interactive map of all rides
  - _folium_map.ipynb_

### scripts
  - pymongo_scripts.py
     - helper scripts for interacting with pymongo

  - StravaActivity.py
     - class with attributes of/ calculations for strava activity 
