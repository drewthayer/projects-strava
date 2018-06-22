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

_example: Torrey's peak ski tour_

- maps: lat, lon

<img alt="Torreys map" src="/figs/xy/Torreys Peak ski_xy.png" width="500">

- elevation profiles:

<img alt="Torreys profile" src="/figs/elev_profiles/Torreys Peak ski_elev.png" width="500">

- slope analysis:

<img alt="Torreys" src="/figs/slope_profiles/Torreys Peak ski_slope.png" width='500'>

- speed analysis:

<img alt="Torreys" src="/figs/speed/Torreys Peak ski_speed.png" width='500'>

### technologies:
  - python
    - stravalib
    - pymongo
  - MongoDB
