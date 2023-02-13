#!/usr/bin/python

import pygame
import urllib
from OpenGL.GL import *
from OpenGL.GLU import *
from math import radians
from pygame.locals import *
from digi.xbee.devices import *
import pandas as pd
from scipy.spatial.transform import Rotation
import math
import re
import time


ser = serial.Serial('COM6', 115200, timeout=0)

ax = ay = az = 0.0

yaw = []
pitch = []
roll = []


SCREEN_SIZE = (800, 600)
SCALAR = .5
SCALAR2 = 0.2


def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.001, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 1.0, -5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0));


def quaternion_to_euler(q):
    global ax, ay, az
    yaw = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
    pitch = -math.sin(2.0 * (q[1] * q[3] - q[0] * q[2]))
    roll = math.atan2(2.0 * (q[0] * q[1] + q[2] * q[3]), q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3])
    pitch *= 180.0 / math.pi
    yaw *= 180.0 / math.pi
    yaw -= 4.31  # Declination at İstanbul 4 degress 31 min
    roll *= 180.0 / math.pi

    az = yaw
    ay = pitch
    ax = roll


def read_data():
    global ax,ay,az
    try:
        data = ser.readline().decode('utf8')
        if(re.search('\$E&',data)):
            packageData = data.split('&')
            if len(packageData) == 17:
                quatW = int(packageData[12])/16384
                quatX = int(packageData[13])/16384
                quatY = int(packageData[14])/16384
                quatZ = int(packageData[15])/16384
                quaternion_to_euler([quatW, quatX, quatY, quatZ])
    except ValueError:
        print("!!!RF PAYLOAD ERROR!!!")

def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    resize(*SCREEN_SIZE)
    init()
    clock = pygame.time.Clock()
    cube = Cube((0.0, 0.0, 0.0), (.5, .5, .7))
    angle = 0

    while True:
        then = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return
        time.sleep(0.01)
        read_data()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor((1., 1., 1.))
        glLineWidth(1)
        glBegin(GL_LINES)

        for x in range(-20, 22, 2):
            glVertex3f(x / 10., -1, -1)
            glVertex3f(x / 10., -1, 1)

        for x in range(-20, 22, 2):
            glVertex3f(x / 10., -1, 1)
            glVertex3f(x / 10., 1, 1)

        for z in range(-10, 12, 2):
            glVertex3f(-2, -1, z / 10.)
            glVertex3f(2, -1, z / 10.)

        for z in range(-10, 12, 2):
            glVertex3f(-2, -1, z / 10.)
            glVertex3f(-2, 1, z / 10.)

        for z in range(-10, 12, 2):
            glVertex3f(2, -1, z / 10.)
            glVertex3f(2, 1, z / 10.)

        for y in range(-10, 12, 2):
            glVertex3f(-2, y / 10., 1)
            glVertex3f(2, y / 10., 1)

        for y in range(-10, 12, 2):
            glVertex3f(-2, y / 10., 1)
            glVertex3f(-2, y / 10., -1)

        for y in range(-10, 12, 2):
            glVertex3f(2, y / 10., 1)
            glVertex3f(2, y / 10., -1)

        glEnd()
        glPushMatrix()
        glRotate(float(ax), 1, 0, 0)
        glRotate(-float(ay), 0, 0, 1)
        cube.render()
        glPopMatrix()
        pygame.display.flip()


class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # Cube information
    num_faces = 6

    vertices = [(-1.0, -0.05, 0.5),
                (1.0, -0.05, 0.5),
                (1.0, 0.05, 0.5),
                (-1.0, 0.05, 0.5),
                (-1.0, -0.05, -0.5),
                (1.0, -0.05, -0.5),
                (1.0, 0.05, -0.5),
                (-1.0, 0.05, -0.5)]

    normals = [(0.0, 0.0, +1.0),  # front
               (0.0, 0.0, -1.0),  # back
               (+1.0, 0.0, 0.0),  # right
               (-1.0, 0.0, 0.0),  # left
               (0.0, +1.0, 0.0),  # top
               (0.0, -1.0, 0.0)]  # bottom

    vertex_indices = [(0, 1, 2, 3),  # front
                      (4, 5, 6, 7),  # back
                      (1, 5, 6, 2),  # right
                      (0, 4, 7, 3),  # left
                      (3, 2, 6, 7),  # top
                      (0, 1, 5, 4)]  # bottom

    def render(self):
        then = pygame.time.get_ticks()
        glColor(self.color)

        vertices = self.vertices

        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)

        for face_no in range(self.num_faces):
            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glVertex(vertices[v1])
            glVertex(vertices[v2])
            glVertex(vertices[v3])
            glVertex(vertices[v4])
        glEnd()


if __name__ == "__main__":
    run()
