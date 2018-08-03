# server.py

import json
import requests
import pandas as pd
import numpy as np
import time, datetime
from datetime import timedelta
from geojson import Point, Feature, FeatureCollection

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

# TODO: Move this to a separate fetch to improve page load times
# Queries NYC Open Data and returns a Pandas DataFrame
def get_crash_data(day_range):

    # NYC DATA QUERY

    start_time = time.time()
    
    print('Day range: ', day_range)
    
    today = datetime.datetime.now()
    days_ago = today - timedelta(day_range)

    url = 'https://data.cityofnewyork.us/resource/qiz3-axqb.json?'\
          '$limit=100000'\
          '&$where=date%20between%20%27' + days_ago.isoformat() + '%27%20'\
          'and%20%27' + today.isoformat() + '%27'
    
    crash_data = pd.read_json(url)

    elapsed_time = time.time() - start_time

    print('Data fetch: ', elapsed_time)
    
    return crash_data

def get_crash_data_points(crash_data):

    start_time = time.time()
    
    crash_df = pd.DataFrame({
        'Date' : crash_data.date,
        'Location' : crash_data.location,
        'Cause' : crash_data.contributing_factor_vehicle_1})
    #account for NaN
    crash_df = crash_df.replace(np.nan, 'Unspecified', regex=True)
    crash_data_points = []
    for index, crash in crash_df.iterrows():
        try:
            coordinates = crash["Location"]["coordinates"]
            point = Point([coordinates[0], coordinates[1]])
            properties = {
                'title': crash["Date"].__str__(),
                'description': crash["Cause"],
                }
            feature = Feature(geometry = point, properties = properties)
            crash_data_points.append(feature)
        except:
            continue

    num_data_points = len(crash_data_points)
    
    crash_data_points = FeatureCollection(crash_data_points)  
  
    # Write GeoJSON data to a file
    with open('crash_data.geojson', 'w') as outfile:
        json.dump(crash_data_points, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    elapsed_time = time.time() - start_time

    print('Data clean: ', elapsed_time)
    print('Number of data points: ', num_data_points)

    return crash_data_points

@app.route('/')
def index():
    
    # default
    day_range = 14
    
    crash_data = get_crash_data(day_range)
    crash_data_points = get_crash_data_points(crash_data)

    return render_template('index.html', 
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        crash_data_points = crash_data_points,
    )

@app.route('/days/<int:day_range>')
def day_range(day_range):
    
    crash_data = get_crash_data(day_range)
    crash_data_points = get_crash_data_points(crash_data)

    return render_template('index.html', 
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        crash_data_points = crash_data_points,
    )

if __name__ == "__main__":
    app.run()
