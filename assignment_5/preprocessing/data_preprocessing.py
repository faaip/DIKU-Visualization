# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 18:45:00 2019

@author: gusta
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
from pathlib import Path

# get the file path

data_path = 'C:/Users/gusta/Desktop/IT_and_cognition/Visualization/Final project/' #Write the data path with '/' and it will be reformulated to correct operating system
data_folder = Path(data_path)
data_name = 'Placeringshistorik.json'
file_to_open = data_folder / data_name

# Load the data

with open(file_to_open, 'r') as read_file:
    data = json.load(read_file)

# Decide how many points should be used (Default all points)

number_of_points = len(data['locations'])
#number_of_points = 1000

# Get all activities as a list. If no activity is present give it a NA value

activities = []
for i in range(len(data['locations'])):
    if 'activity' in data['locations'][i].keys():
        act = data['locations'][i]['activity'][0]['activity'][0]['type']
        activities.append(act)
    else:
        activities.append('NA')

# Define a function that takes a timestamp in Ms and returns a date in iso 8601 format
def date_maker(time_stamp):

    timestamp = round ( int( time_stamp) / 1000 )

    date = datetime.fromtimestamp(timestamp).isoformat() 

    return date

# Conver time stamp to a date iso 8601 format

dates = [ date_maker( x['timestampMs']) for x in data['locations']]

# Add year and month as features
def year_maker(time_stamp, date_type='Year'):
    '''Function that takes a time_stamp and returns a year or month as string '''
    if date_type == 'Year':
        timestampS = round(int(time_stamp) / 1000)
        date = datetime.fromtimestamp(timestampS)
        date_value = date.year

    elif date_type == 'Month':
        timestampS = round(int(time_stamp) / 1000)
        date = datetime.fromtimestamp(timestampS)
        date_value = date.strftime("%B")

    return date_value

# get year as a lists
years = [year_maker(x['timestampMs']) for x in data['locations']]

# get months as a list
months = [year_maker(x['timestampMs'], date_type='Month') for x in data['locations']]

'''Adding duration to each location point ''' 

# Get all time stamps as a numpy array

TimeStamps = np.asarray([int(point['timestampMs']) for point in data['locations'][1:]]) # Get all timestamps beside the last one
TimeStampsShift = np.asarray([int(point['timestampMs']) for point in data['locations'][:-1]]) # get all timestamps beside the first one

# Difference between timestamps in seconds

diff = (TimeStampsShift - TimeStamps) / 1000

# Remove outliers. Certain durations are too high
# Maybe if the phone was turned off for a few days
# Through visual inspection it is clear the the diffs above 415sec can be considered outliers

outlier = 415 # outlier

outlierBool = diff > outlier

# Estimate mean when outliers are not included
newMean = np.mean(diff[diff < outlier])

mask = np.where(outlierBool) # Turn boolean into index of outliers

diff[mask] = newMean # Replace outliers with the mean estimted without outliers

# Create the zip object that contains the preocessed information that has to be put into the geojson
# 0: dic with long and lat
# 1: list with duration in sec
# 2: activity type
# 3: date
# 4: years
# 5: months

zip_object = zip(data['locations'][0:number_of_points], 
        diff[0:number_of_points], 
        activities[0:number_of_points], 
        dates[0:number_of_points],
        years[0:number_of_points],
        months[0:number_of_points])

geojson = {
        "type": "FeatureCollection",
        "features":[
                {
                        "type":"Feature","properties":{"durationSec":d[1],
                        "activity": d[2],
                        "date": d[3],
                        "year": d[4],
                        "month":d[5]}, 
                                "geometry":{"type":"Point",
                                "coordinates": [d[0]["longitudeE7"] / 1e7, 
                                                d[0]["latitudeE7"] / 1e7],
                                },
                                
                                } for i,d in enumerate(zip_object) if i % 5 == 0 ] #keep every 5 point for performance reasons
    }
    

# add a utility that allowes you to dumb the geojson file where you want

string = json.dumps(geojson, separators=(',', ':')) # Convert the geojson to a string for export purposes

# Path to where you want to export the file
export_folder = 'C:/Users/gusta/Desktop/IT_and_cognition/Visualization/Final project/'
# export_folder = 'C:/Users/gusta/Desktop/IT_and_cognition/Visualization/Final project/'
export_path = Path(export_folder)
export_file_name = 'placeringsoversigt_medium.geojson'
export_path_name = export_path / export_file_name

#Export the file as geojson to specified location
    
with open (export_path_name, 'w') as text_file:
    print(string, file=text_file)


