import re
import codecs
from gmplot import *
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib import style
from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt
import time
import json
import datetime
from matplotlib.animation import FuncAnimation
import itertools
from numpy import diff
import scipy.integrate
import csv
import simplekml
import pandas
import datetime
from datetime import timedelta

plt.style.use('seaborn-pastel')

accValX = []
accValY = []
accValZ = []
magValX = []
magValY = []
magValZ = []
gyroValX = []
gyroValY = []
gyroValZ = []
diffInMeter = []
diffInMeter.append(0)
lat = []
lon = []
hdop = []
timeSeries = []


gSpeed = []
counter = 0
measurements = []

#functions
def measureDistance(lat1, lon1, lat2, lon2): #mearure the distance between two coordinates
    R = 6378.137; # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180;
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180;
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    d = R * c;
    return d * 1000; #meters

    
csvval = csv.DictReader(open("test_iuc_halil_1.csv", "r"), delimiter = ',')
content = []
content.extend(csvval) #

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

content.sort(key=lambda x:x['device_date'])   #if data is not sorted, sort by date

#id,"device_id","fix","hdop","latitude","longitude","velocity","heart_rate","acc_x","acc_y","acc_z","quat_w","quat_x","quat_y","quat_z","device_date","db_date"
for line in content:
    if(line["fix"] == "1" or line["fix"] == "2") and line["device_id"] == "7" and float(line["hdop"]) < 20:
        lat.append(float(line["latitude"]))
        lon.append(float(line["longitude"]))
        hdop.append(float(line["hdop"]))
        gSpeed.append(float(line["hdop"])*1.852) # knots to km/s
        #timeSeries.append(datetime.datetime.strptime((line["device_date"])[:19], '%Y-%m-%d %H:%M:%S').time())
        counter += 1
        timeSeries.append(counter)
        measurements.append([float(line["latitude"]),float(line["longitude"])])


measurements = np.asarray(measurements)

initial_state_mean = [measurements[0, 0],
                      0,
                      measurements[0, 1],
                      0]

transition_matrix = [[1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

observation_matrix = [[1, 0, 0, 0],
                      [0, 0, 1, 0]]
print('Starting Kalman Iterations...')
kf1 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean)

kf1 = kf1.em(measurements, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)

kf2 = KalmanFilter(transition_matrices = transition_matrix,
                  observation_matrices = observation_matrix,
                  initial_state_mean = initial_state_mean,
                  observation_covariance = 100*kf1.observation_covariance,
                  em_vars=['transition_covariance', 'initial_state_covariance'])

kf2 = kf2.em(measurements, n_iter=5)
(smoothed_state_means, smoothed_state_covariances)  = kf2.smooth(measurements)

print('Kalman Iterations Has Been Done...')
print('Updating Maps...')
# Draw the GPS line On Google Maps on a HTML page.
gmap = gmplot.GoogleMapPlotter(lat[0], lon[0], 20)
gmap.plot(smoothed_state_means[:, 0],smoothed_state_means[:, 2],edge_width=6,color='cornflowerblue')
gmap.scatter(measurements[:, 0],measurements[:, 1],'#fb9214', size = 0.4, marker = False)
gmap.coloricon
gmap.apikey = "AIzaSyCLfWwWJhjH4hbph9N6X3GTgWr4bboLUQ0"
gmap.draw( "kalman.html")
plt.show()
print('---END---')
