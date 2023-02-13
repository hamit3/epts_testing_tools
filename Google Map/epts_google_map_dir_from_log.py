import webbrowser
import re
import codecs
from gmplot import *
import matplotlib.pyplot as plt
import math
import numpy as np
from matplotlib import style

style.use('dark_background')


diffInMeter = []
diffInMeter.append(0)
lat = []
lon = []
hdop = []
timeSeries = []
counter = 0


# Read and decode the log data    
f = open("gps_log.txt", 'r', encoding="utf-8", errors='ignore');
print('File Openned')
file_content = f.readlines()
f.close()
print('File Closed')
line_qty = len(file_content)
content = [x.strip() for x in file_content]

for file_lines in content:
    x = file_lines
    cntStart = 0
    cntEnd = 0
    fDataValid = False
    lineEndChars = re.search('D$', x)
    lineStartChars =re.search(r'$E', x )
    endOfFile = re.search('&', x)
         
for all_content in content:
    if(all_content):
        packageData = all_content.split('&')
        if(len(packageData) == 16):
            if(packageData[2] == '1' or packageData[2] == '2'):  # GPS or DGPS fix ?
                counter += 1
                timeSeries.append(counter)
                lat.append(float(packageData[4]))
                lon.append(float(packageData[5]))

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


# Draw the GPS line On Google Maps on a HTML page.
gmap = gmplot.GoogleMapPlotter(lat[0], lon[0], 20)
gmap.plot(lat,lon,edge_width=1,color='cornflowerblue')
gmap.scatter(lat,lon,'#fb9214', size = 1, marker = False)
gmap.coloricon
gmap.apikey = "AIzaSyCLfWwWJhjH4hbph9N6X3GTgWr4bboLUQ0"
gmap.draw( "direction.html")
plt.show()
print('---END---')

