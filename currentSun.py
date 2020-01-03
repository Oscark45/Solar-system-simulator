# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

"""
Author:     Oscar Kaatranen
Created:    %(date)$
Modified:   %(date)$ 

Description

This file tests out the current orientation of the sun. Supposed to be a 
replica of what was the first visualization attempt with the 5 vectors.

"""

import numpy as np
import matplotlib.pyplot as plt
import urllib
plt.close('all')
from numpy.random import random as rng

import math as math

import sys

# Libraries for time
from datetime import datetime
from datetime import date
from datetime import timedelta
import time

import localSun as current

clat = 30
lon = 0

plt.close('all')

timeNow = np.array([datetime.now()], dtype = 'datetime64[s]') # Current time
timeTest = np.array([np.datetime64('2018-12-21T04:19:00', 's')]) # This way you can put any time you want
timeTest = np.array([np.datetime64('2019-07-28T00:00:00', 's')])

print('Here it all begins\n')
print('Time is now {:} from this laptop. Thus timezones might screw up but will be fixed later.\n'.format(str(timeNow)))
print('(1) We are at colatitude {:} degrees and longitude {:} degrees\n'.format(clat, lon))

sunNow = current.localSun(clat = clat, lon = lon, time = timeNow)

print('Currently the observers vectors are (Radial, Polar, Azimuthal) \n {:}\n'.format(sunNow.obsV()))

print('The sun is currently shining directly at colatitude {:5f}.'.format(math.degrees(sunNow.latSun())))
print('Thus at the south pole it is at {:2f} degrees with respect to the horizon.\n'.format(math.degrees(sunNow.latSun()) - 90))

print('At this colatitude ({:d}) and longitude ({:d}) the sun is at {:.6f} degrees with respect to the horizon.\n'\
      .format(clat, lon, math.degrees(sunNow.altitude())))
print("The suns azimuth is {:.6f}".format(math.degrees(sunNow.azimuth())))

# Plot the Earth-Sun system
fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D # This is apparently needed for the '3d' next line
ax = fig.gca(projection='3d')
ax.set_xlim3d(-1.5, 1.5)
ax.set_ylim3d(-1.5, 1.5)
ax.set_zlim3d(-1.5, 1.5)

colors = list(['r', 'g', 'b', 'k', 'y', 'm'])
# Red - observers radial vector
# Green - observers polar vector
# Blue - observers azimuthal vector
# Black - Tilt vector
# Yellow - Earth's plane vector pointing towards the sun
# Magenta - Earth's position vector pointing from the sun

import itertools
j = 0 

# Earth's position vector. Used for coordinates and direction
orientationY = sunNow.orientY
posEarth = current.earthDir(np.array([orientationY]))*1.2

# What are the vector lengths we want
lengths = np.array([0.5, 0.5, 0.5, 0.9, 0.8, 0.9])

# Iterate through the observers vectors, the tilt vector and azSun() and put them where the Earth is
for v in itertools.chain(sunNow.obsV(), np.array([[current.tiltV()]]), np.array([sunNow.azSun()])):
    
    # itertools.chain(...) allows us to go through many vectors at once. Handy
    ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2] , v[0][0], v[0][1], v[0][2] \
              , length = lengths[j], normalize = False, color = '{:}'.format(colors[j]))
    j += 1

# Plot several plane vectors to give an illustration about the Earth's equator plane.
for orientation in np.linspace(0, 2*np.pi, num=100):
    earthVector = current.planeV(np.array([orientation]))
    ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2], earthVector[0][0], earthVector[0][1], \
              earthVector[0][2], length = 0.25 , normalize = False, color = 'k')

# Plot the coordinate axes
for v in np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) :
    ax.quiver(0, 0, 0, v[0], v[1], v[2], length = 0.5, normalize = False, color = 'k')

# Plot the position vector of Earth
w = current.earthDir(np.array([orientationY]))
v = current.sunV(np.array([orientationY]))
ax.quiver(0, 0, 0, w[0][0], w[0][1], w[0][2], length = 0.8, normalize = False, color = 'm')

print('Seems to be working fine!\n')
print("Angle between azSun() and polarV():")
a = sunNow.obsV()[1]
print(np.degrees(current.angleVectors(sunNow.obsV()[1], sunNow.azSun())))
b = sunNow.obsV()[2]
print("Angle between azSun() and azimuthalV():")
print(np.degrees(current.angleVectors(sunNow.obsV()[2], sunNow.azSun())))

