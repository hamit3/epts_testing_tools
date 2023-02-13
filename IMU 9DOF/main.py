import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
import pygame
import urllib
from math import radians
import re
import time
import serial

ser = serial.Serial('COM6', 115200, timeout=0)

quatW = 0
quatX = 0
quatY = 0
quatZ = 0

PI=3.1415926


def resizewin(width, height):
    """
    For resizing window
    """
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def drawText(position, textString, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def quat_to_ypr(q):
    yaw = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
    pitch = -math.sin(2.0 * (q[1] * q[3] - q[0] * q[2]))
    roll = math.atan2(2.0 * (q[0] * q[1] + q[2] * q[3]), q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3])
    pitch *= 180.0 / math.pi
    yaw *= 180.0 / math.pi
    yaw -= -5.49  # Declination at İstanbul, 5 degress 49 min  ?
    roll *= 180.0 / math.pi
    return [yaw, pitch, roll]


def read_data():
    global quatW,quatX,quatY,quatZ
    while True:
        try:
            data = ser.readline(ser.inWaiting()).decode('utf8')
            if '\n' in data:
                if(re.search('\$E&',data)):
                    packageData = data.split('&')
                    if len(packageData) >= 17:
                        quatW = float(int(packageData[12])/16384)
                        quatX = float(int(packageData[13])/16384)
                        quatY = float(int(packageData[14])/16384)
                        quatZ = float(int(packageData[15])/16384)
                        break
        except ValueError:
            print("!!!RF PAYLOAD ERROR!!!")
            continue
        break


def draw():
    read_data()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)

    drawText((-2.6, 1.8, 2), "EPTS", 18)
    drawText((-2.6, 1.6, 2), "Module to visualize quaternion data", 16)
    drawText((-2.6, -2, 2), "Press Escape to exit.", 16)

    [yaw, pitch, roll] = quat_to_ypr([quatW, quatX, quatY, quatZ])
    #print(yaw,pitch,roll)
    drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" % (yaw, pitch, roll), 16)
    glRotatef(2 * math.acos(quatW) * 180.00 / math.pi, quatX, quatZ, -1 * quatY)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)
    glEnd()



video_flags = OPENGL | DOUBLEBUF
pygame.init()
screen = pygame.display.set_mode((1024, 720), video_flags)
pygame.display.set_caption("PyTeapot IMU orientation visualization")
resizewin(1024, 720)
init()

def visualization_main():
    while True:
        draw()
        pygame.display.flip()


if __name__ == '__main__':
    visualization_main()
