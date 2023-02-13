import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import serial
import time
import re

#style.use('dark_background')
ser = serial.Serial('COM6', 115200, timeout=0)

fig = plt.figure()
img = plt.imread("heartratezone.png")
ax1 = fig.add_subplot(1,1,1)
heartRateSeries = []
timeSeries = []
counter = 0

def animate(i):
    global heartRateSeries, timeSeries, counter
    try:
        data = ser.readline().decode('utf8')
        if(re.search('\$E&',data)):
            packageData = data.split('&')
            
            if len(packageData) == 17 and isinstance(int(packageData[8]), int):
                heartRate = int(packageData[8])
                counter += 1
                heartRateSeries.append(heartRate)
                timeSeries.append(counter)          
    except ValueError:
        print("!!!READ COM PORT ERROR!!!")

    ax1.clear()
    ax1.set_ylabel('HeartRate')
    ax1.set_title('HeartRate Change')
    line, = ax1.plot(timeSeries[-250:], heartRateSeries[-250:], color='blue', label='heartRateVal', lw=4)
    ax1.axis([counter-250, counter, 0, 200])
    ax1.imshow(img, extent=[counter-250, counter, 0, 200])
    ax1.legend()

ani = animation.FuncAnimation(fig, animate, frames = 1, interval=1)
plt.show()
ser.close()
