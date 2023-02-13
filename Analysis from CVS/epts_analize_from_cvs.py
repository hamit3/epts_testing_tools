# Implement and Analysis Data from comma seperated values (csv)
import json
import datetime
import re
import codecs
from gmplot import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import itertools
import math
from numpy import diff
import scipy.integrate
import csv
import simplekml
import pandas
import datetime
from datetime import timedelta
import statistics

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
Zone25 = []
Zone20to25 = []
Zone15to20 = []
diffInMeterUpper25 = []
diffInMeter20to25 = []
diffInMeter15to20 = []
diffInMeter = []
diffInMeter.append(0)
diffInMeterUpper25.append(0)
diffInMeter20to25.append(0)
diffInMeter15to20.append(0)

lat = []
lon = []
hdop = []
velocity = []
fix = []
timeSeries = []
accX = []

# ADD DEVICE ID's TO ANALYZE
devices = ['3', '7','9']

#PACKAGE order -- #id,"device_id","fix","hdop","latitude","longitude","velocity","heart_rate","acc_x","acc_y","acc_z","quat_w","quat_x","quat_y","quat_z","device_date","db_date" 

#functions
def measureDistance(lat1, lon1, lat2, lon2): #mearure the distance between two coordinates
    R = 6378.137; # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180;
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180;
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
    d = R * c;
    return d * 1000; #meters

    
csvval = csv.DictReader(open("test_iuc_halil.csv", "r"), delimiter = ',')
content = []
content.extend(csvval) #

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

content.sort(key=lambda x:x['device_date'])   #if data is not sorted, sort by date

for device in devices:
    lat = []
    lon = []
    hdop = []
    velocity = []
    fix = []
    timeSeries = []
    accX = []
    diffInMeter = []
    Zone25 = []
    Zone20to25 = []
    Zone15to20 = []
    diffInMeterUpper25 = []
    diffInMeter20to25 = []
    diffInMeter15to20 = []    
    print('DEVICE ID: %s' %device)
    for line in content:
        if(line["fix"] == "1" or line["fix"] == "2") and line["device_id"] == device:
            lat.append(float(line["latitude"]))
            lon.append(float(line["longitude"]))
            hdop.append(float(line["hdop"]))
            velocity.append(float(line["velocity"])*1.852)
            fix.append(float(line["fix"]))
            accX.append(float(line["acc_x"]))
            timeSeries.append(datetime.datetime.strptime((line["device_date"])[:19], '%Y-%m-%d %H:%M:%S').time())


    tdelta = ((timeSeries[-1].hour*60*60 + timeSeries[-1].minute*60 + timeSeries[-1].second) - (timeSeries[0].hour*60*60 + timeSeries[0].minute*60 + timeSeries[0].second))/60
    print("Training time: %d min" %tdelta)
    #print("Total data package: ",len(timeSeries))
    #print("Avarage Data Sample Number in Seconds : ",len(timeSeries)/tdelta)


    diffBetweenMeasurements = [measureDistance(lat[i+1],lon[i+1],lat[i],lon[i]) for i in range(len(lon)-1)]
    for i in range(len(lon)-1):
        if diffBetweenMeasurements[i] < 100:
            diffInMeter.append(diffBetweenMeasurements[i])
            
    Zone25= [measureDistance(lat[i+1],lon[i+1],lat[i],lon[i]) for i in range(len(lon)-1)]
    for i in range(len(lon)-1):
        if velocity[i] >= 25:
            diffInMeterUpper25.append(Zone25[i])
    Zone20to25= [measureDistance(lat[i+1],lon[i+1],lat[i],lon[i]) for i in range(len(lon)-1)]
    for i in range(len(lon)-1):
        if velocity[i] >= 20 and velocity[i] < 25:
            diffInMeter20to25.append(Zone20to25[i])
    Zone15to20= [measureDistance(lat[i+1],lon[i+1],lat[i],lon[i]) for i in range(len(lon)-1)]
    for i in range(len(lon)-1):
        if velocity[i] >= 15 and velocity[i] < 20:
            diffInMeter15to20.append(Zone15to20[i])              
    print('Total Distance: %d meters ' %(sum(diffInMeter)))
    print('Total Distance - ( velocity > 25) : %d meters ' %(sum(diffInMeterUpper25)))
    print('Total Distance - ( velocity > 20 and velocity < 25 ) : %d meters ' %(sum(diffInMeter20to25)))
    print('Total Distance - ( velocity > 15 and velocity < 20 ) : %d meters ' %(sum(diffInMeter15to20)))     
    #print('Std of measurements: ',np.std(diffInMeter))
    #print('Max difference between 2 measurements: ',max(diffInMeter))
    print('Max speed: %.2f km/s  ' %(max(velocity)))
    print('Avarage Speed: %.2f km/s '%(np.mean(diffInMeter)))
    print('---------------------')




    fig1 = plt.figure(int(device))
    ax = fig1.add_subplot(211)
    ax.set_title('Player_{d}'.format(d=int(device)))
    ax.set_ylabel('Hdop')
    ax.plot(timeSeries,hdop, 'r', timeSeries, fix, 'b', lw=1)

    ax2 = fig1.add_subplot(212)
    ax2.set_ylabel('velocity')
    line, = ax2.plot(timeSeries,velocity, color='blue', label='velocity', lw=1)
    ax2.legend()

    # Draw the GPS line On Google Maps on a HTML page.
    gmap = gmplot.GoogleMapPlotter(lat[0], lon[0], 20)
    gmap.scatter(lat,lon,'#fb9214', size = .1, marker = False)
    gmap.heatmap(lat,lon)
    gmap.plot(lat,lon,'#ff33cc', edge_width=1)
    gmap.coloricon
    gmap.apikey = "AIzaSyCLfWwWJhjH4hbph9N6X3GTgWr4bboLUQ0"
    gmap.draw( "direction_device_{d}.html".format(d=int(device)))



# Show Figures
print('---SHOW FIGURES---')
#fig.tight_layout(pad=1.0)
plt.show()
print('---END---')

