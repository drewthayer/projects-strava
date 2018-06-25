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
  - MongoDB
