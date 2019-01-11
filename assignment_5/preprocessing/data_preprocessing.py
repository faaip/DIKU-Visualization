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

data_path = 'C:/Users/user/Desktop/IT and Cognition/Visualisation/finalProject/' #Write the data path with '/' and it will be reformulated to correct operating system
data_folder = Path(data_path)
data_name = 'Placeringshistorik.json'
file_to_open = data_folder / data_name

# Load the data

with open(file_to_open, 'r') as read_file:
    data = json.load(read_file)
    
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

geojson = {
        "type": "FeatureCollection",
        "features":[
                {
                        "type":"Feature","properties":{"durationSec":d[1]}, 
                                "geometry":{"type":"Point",
                                "coordinates": [round(d[0]["longitudeE7"] / 1e7,5), 
                                                round(d[0]["latitudeE7"] / 1e7,5)],
                                },
                                
                                } for d in zip(data['locations'][0:500],diff[0:500])] 
    }
    

# add a utility that allowes you to dumb the geojson file where you want

string = json.dumps(geojson, separators=(',', ':')) # Convert the geojson to a string for export purposes

# Path to where you want to export the file
export_folder = 'C:/Users/user/Desktop/IT and Cognition/Visualisation/finalProject/'
export_path = Path(export_folder)
export_file_name = 'placeringsoversigt.geojson'
export_path_name = export_path / export_file_name


#Export the file as geojson to specified location
    
with open (export_path_name, 'w') as text_file:
    print(string, file=text_file)



















