# -*- coding: utf-8 -*-
"""
Created on Sun May 24 12:57:11 2020

@author: Oscar
"""

# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

import math as math
import help_functions as hp

# Libraries for time
from datetime import datetime
from datetime import date
from datetime import timedelta
import time

import localSun as current

clat = 30
lon = 0
ecc = 0.567

plt.close('all')

timeNow = np.array([datetime.now()], dtype = 'datetime64[s]') # Current time
timeTest = np.array([np.datetime64('2018-12-21T04:19:00', 's')]) # This way you can put any time you want

start0 = np.array([np.datetime64('2018-12-22T00:00:00', 's')]) # 2019 Winter Solstice (UTC)
perihelion0 = np.array([np.datetime64('2019-03-22T00:00:00', 's')]) # 2020 perihelion (UTC)
timeTest = np.array([np.datetime64('2019-03-22T00:00:00', 's')]) # This way you can put any time you want
#timeTest = perihelion0
#timeTest = start0
#perihelion0 = start0


print('Here it all begins\n')
print('Time is now {:} from this laptop. Thus timezones might screw up but will be fixed later.\n'.format(str(timeNow)))
print('(1) We are at colatitude {:} degrees and longitude {:} degrees\n'.format(clat, lon))

sunNow = current.localSun(clat = clat, lon = lon, time = timeTest, ecc = ecc, perihelion = perihelion0, start = start0)


print('The sun is currently shining directly at colatitude {:5f}.'.format(math.degrees(sunNow.latSun())))
print('Thus at the south pole it is at {:2f} degrees with respect to the horizon.\n'.format(math.degrees(sunNow.latSun()) - 90))

print('At this colatitude ({:d}) and longitude ({:d}) the sun is at {:.6f} degrees with respect to the horizon.\n'\
      .format(clat, lon, np.degrees(sunNow.altitude()[0])))

# Plot the Earth-Sun system
fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D # This is apparently needed for the '3d' next line
ax = fig.gca(projection='3d')
ax.set_xlim3d(-2, 2)
ax.set_ylim3d(-2, 2)
ax.set_zlim3d(-2, 2)

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
orientationY = sunNow.angleY
posEarth = hp.earthDir(np.array([orientationY]), r = sunNow.radii[0])

# What are the vector lengths we want
lengths = np.array([0.5, 0.5, 0.5, 0.9, 0.8, 0.9])


# Plot several plane vectors to give an illustration about the Earth's equator plane.
for orientation in np.linspace(0, 2*np.pi, num=20):
    earthVector = hp.planeV(np.array([orientation]))
    ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2], earthVector[0][0], earthVector[0][1], \
              earthVector[0][2], length = 0.25 , normalize = False, color = 'green')

# Plot the coordinate axes
for v in np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) :
    ax.quiver(0, 0, 0, v[0], v[1], v[2], length = 0.5, normalize = False, color = 'k')

# Plot the position vector of Earth

w = hp.earthDir(np.array([orientationY]))

ax.quiver(0, 0, 0, w[0][0], w[0][1], w[0][2], length = 0.8, normalize = False, color = 'm')

ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2],\
          hp.tiltV()[0], hp.tiltV()[1], hp.tiltV()[2], length = 1.2, color ='black')

x,y,z = sunNow.radialV()

ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2],\
          x,y,z, length = 0.9, color ='red')


# Plot the orbit
angle = np.linspace(0, 2*np.pi, num = 200)
xs = np.cos(angle)*hp.polarEllipse(angle, sunNow.ecc, advance = sunNow.advance)

ys = np.sin(angle)*hp.polarEllipse(angle, sunNow.ecc, advance = sunNow.advance)
ax.scatter(xs,ys, marker = '.')
