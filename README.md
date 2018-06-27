### Strava visualization project
#### goals: download my data with the strava api, make visualizations, analyze activities

steps:
  1. call strava database with _stravalib_ python api
  2. download recent activities for my user account
  3. save activities to a Mongo database with _pymongo_
    - activities are nested dictionaries
    - Mongo, an unstructured database, is ideal for storing this data
  4. store each activity in a _StravaActivity_ class for easy calculations and plotting
  5. calculate metrics and make visualizations

### heatmap of activities:
<img alt="state map" src="/figs/map_state.png" width="500">

### activity summaries:
~~~
activity: North Table
distance: 7.75 mi
time: 0.97 hr
average speed: 8.02 mph
max speed = 11.20 mph

activity: Golden loop
distance: 23.00 mi
time: 1.59 hr
average speed: 14.42 mph
max speed = 15.15 mph

activity: Checking out vail riding
distance: 18.99 mi
time: 3.39 hr
average speed: 5.60 mph
max speed = 10.67 mph

activity: Lookout climb with the nation of Tuck-menace-stan
distance: 34.07 mi
time: 2.41 hr
average speed: 14.13 mph
max speed = 15.75 mph

activity: Too long?
distance: 28.55 mi
time: 8.03 hr
average speed: 3.55 mph
max speed = 11.18 mph

activity: Dr  park rally!
distance: 18.53 mi
time: 3.06 hr
average speed: 6.06 mph
max speed = 11.90 mph

activity: N Table
distance: 7.46 mi
time: 1.17 hr
average speed: 6.37 mph
max speed = 12.20 mph

activity: Best trail ever?
distance: 14.99 mi
time: 1.96 hr
average speed: 7.64 mph
max speed = 10.15 mph

activity: Hay Park
distance: 9.26 mi
time: 2.61 hr
average speed: 3.54 mph
max speed = 11.00 mph

activity: Carbondale riding whoops wrong climb
distance: 8.33 mi
time: 2.86 hr
average speed: 2.91 mph
max speed = 14.80 mph
~~~


### activity visualizations:

_example: Doctor Park mountain ride near Crested Butte_

- maps view:

<img alt="Dr map" src="/figs/xy/Dr_park_rally_xy.png" width="500">

- elevation profiles:

<img alt="Dr profile" src="/figs/elev_profiles/Dr_park_rally_elev.png" width="500">

- slope analysis:

<img alt="Dr slope" src="/figs/slope_profiles/Dr_park_rally_slope.png" width='500'>

- speed analysis:

<img alt="Dr park" src="/figs/speed/Dr_park_rally_speed.png" width='500'>

### technologies:
  - python
    - stravalib
    - pymongo
    - folium
  - MongoDB
