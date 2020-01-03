# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

"""
Author:     Oscar Kaatranen
Created:    %(date)$
Modified:   %(date)$ 

Description

Compute the solar radiation distribution over the Earth over one year.

"""

import numpy as np
import matplotlib.pyplot as plt
import localSun as current
from datetime import datetime
import math as math

# Given an array of altitudes, take only those into account that are > 0
def yearSun(altitude):
    
    positives = altitude * (altitude > 0)*(1) # Only wanting those with positive altitude
    
    return np.sin(positives) 

day = 86400 - 86400/366
year = 31536000
idealStart = np.array([np.datetime64('2018-12-22T12:00:00', 's')])
tilt = math.radians(23.44*0 + 49*0 + 90*1)

# Initialize the figure
fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D # This is apparently needed for the '3d' next line
ax = fig.gca(projection='3d')
ax.set_xlim3d(-1.5, 1.5)
ax.set_ylim3d(-1.5, 1.5)
ax.set_zlim3d(-1.5, 1.5)

colors = list(['r', 'g', 'b', 'k', 'y', 'm'])

# Plot the coordinate axes
for v in np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) :
    ax.quiver(0, 0, 0, v[0], v[1], v[2], length = 0.5, normalize = False, color = 'k')
    

oneYear =  np.arange('2018-12-21T12:00:00', '2019-12-21T12:00:00', dtype = 'datetime64[30m]')
#oneYear = np.array([np.datetime64('2018-12-22T12:00:00', 's'), np.datetime64('2019-06-23T00:00:00', 's')])

heatVector = np.zeros([181, 1])
i = 0


# Iterate through the 180 degrees latitude
for latitude in np.arange(0, 181):
    latSun = current.localSun(clat = latitude, time = oneYear, tilt = tilt, start = idealStart, day = day, year = year)
    
    heatVector[i] = sum(yearSun(latSun.altitude()))
    i += 1

fig = plt.figure('Heat distribution')
ax = fig.gca()
ax.plot(np.arange(0, 181), heatVector, lw = 2)
ax.set(xlabel='Colatitude', ylabel='Power (arb. units)',
       title='Solar power over a year with {:.2f}$^\circ$ tilt'.format(math.degrees(tilt)))
ax.grid()
ax.set_ylim([0, max(heatVector)*1.1])
plt.show()



