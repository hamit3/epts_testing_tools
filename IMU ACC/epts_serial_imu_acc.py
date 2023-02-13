import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import serial
import time
import re

style.use('dark_background')
ser = serial.Serial('COM6', 115200, timeout=0)

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xs = []
ys = []
zs = []
timeSeries = [];
counter = 0

def animate(i):
    global xs, ys, zs, timeSeries, counter
    try:
        data = ser.readline().decode('utf8')
        if(re.search('\$E&',data)):
            packageData = data.split('&')
            
            if len(packageData) == 17:
                accX = float(packageData[9])/1000
                accY = float(packageData[10])/1000
                accZ = float(packageData[11])/1000
                counter += 1
                xs.append(accX)
                ys.append(accY)
                zs.append(accZ)
                timeSeries.append(counter)         
    except ValueError:
        print("!!!READ COM PORT ERROR!!!")

    ax1.clear()
    ax1.set_ylabel('Accel.(g)')
    ax1.set_title('Accelerometer graph on X,Y,Z axis')
    line, = ax1.plot(timeSeries, xs, color='blue', label='accX', lw=2)
    line, = ax1.plot(timeSeries, ys, color='red', label='accY', lw=2)
    line, = ax1.plot(timeSeries, zs, color='green', label='accZ', lw=2)
    ax1.legend()

ani = animation.FuncAnimation(fig, animate, frames = 1, interval=10)
plt.show()

print('---END---')
