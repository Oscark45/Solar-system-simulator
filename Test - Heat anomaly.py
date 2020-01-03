# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

"""
Author:     Oscar Kaatranen
Created:    %(date)$
Modified:   %(date)$ 

Description

There is some anomaly with the heatVector. It should be completely symmetrical but there's deviation.

"""

import numpy as np
import matplotlib.pyplot as plt
import localSun as current
from datetime import datetime
import math as math

day = 86400 - 86400/366
year = 31536000
idealStart = np.array([np.datetime64('2018-12-22T12:00:00', 's')])

print("(1) Let's first test that methods work for several datetimes.\n")

# Some sanity checks
timeTest = np.arange('2018-06-21T08:00:00', '2020-08-21T09:00:00', dtype = 'datetime64[2678400s]')
tilt = math.radians(23.44*0 + 49*0 + 90*0)
sunTest = current.localSun(time = timeTest, tilt = tilt, day = day, year = year, start = np.datetime64('2018-12-22T12:00:00', 's'))
tiltTest = math.radians(23.44*0 + 49*0)

# Sanity checks
solsSun1 = current.localSun(time = np.array([np.datetime64('2018-12-22T12:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
solsSun2 = current.localSun(time = np.array([np.datetime64('2019-06-23T00:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
solsSun3 = current.localSun(time = np.array([np.datetime64('2019-12-22T12:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
eqSun1 = current.localSun(time = np.array([np.datetime64('2019-03-23T18:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
eqSun2 = current.localSun(time = np.array([np.datetime64('2019-09-22T06:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
eqSun2018 = current.localSun(time = np.array([np.datetime64('2018-09-22T06:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)

print("First a simple sanity check to see that thing is symmetric. What's the situation during the solstices and equinoxes?\n")
print("Winter solstice, altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(solsSun1.altitude()[0]), math.degrees(solsSun1.azimuth()[0])))
print("March equinox, altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(eqSun1.altitude()[0]), math.degrees(eqSun1.azimuth()[0])))
print("Summer solstice, altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(solsSun2.altitude()[0]), math.degrees(solsSun2.azimuth()[0])))
print("September equinox, altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(eqSun2.altitude()[0]), math.degrees(eqSun2.azimuth()[0])))
print("Winter solstice (2019), altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(solsSun3.altitude()[0]), math.degrees(solsSun3.azimuth()[0])))
print("September equinox (2018), altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(eqSun2018.altitude()[0]), math.degrees(eqSun2018.azimuth()[0])))
print("\nEach of these are exact. Great!\n")


fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D # This is apparently needed for the '3d' next line
ax = fig.gca(projection='3d')
ax.set_xlim3d(-1.5, 1.5)
ax.set_ylim3d(-1.5, 1.5)
ax.set_zlim3d(-1.5, 1.5)

colors = list(['r', 'g', 'b', 'k', 'y', 'm'])

import itertools
i = 0
j = 0 

# Earth's position vectors. Used for coordinates and direction
posEarths = current.earthDir(sunTest.orientY)*1.2

# Plot the coordinate axes
for v in np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) :
    ax.quiver(0, 0, 0, v[0], v[1], v[2], length = 0.5, normalize = False, color = 'k')

# Iterate through each vector. After that plot each
for u in posEarths:
    ax.quiver(u[0], u[1], u[2] , sunTest.tiltVec[0], sunTest.tiltVec[1], sunTest.tiltVec[2], length = 0.9 \
              , normalize = False, color = 'k')
   
    # Go through the observers vectors (radia, polar, azimuthal)
    for k in np.arange(0,3):
        ax.quiver(u[0], u[1], u[2] , sunTest.obsV()[k][i][0], sunTest.obsV()[k][i][1], sunTest.obsV()[k][i][2], length = 0.5 \
              , normalize = False, color = '{:}'.format(colors[k]))
    # Sanity check with the altitude angles of the sun during midnight
    print("Altitude angle of the sun: {:.6f} and azimuth: {:.6f}".format(math.degrees(sunTest.altitude()[i]), \
          math.degrees(sunTest.azimuth()[i])))
    i += 1

print("\nMiddays look fine. Great!\n")

print("Now we can do the heat distribution thing\n")

oneYear =  np.arange('2018-12-21T12:00:00', '2019-12-21T12:00:00', dtype = 'datetime64[30m]')
#oneYear = np.array([np.datetime64('2018-12-22T12:00:00', 's'), np.datetime64('2019-06-23T00:00:00', 's')])

# Given an array of altitudes, take only those into account that are > 0
def yearSun(altitude):
    
    positives = altitude * (altitude > 0)*(1) # Only wanting those with positive altitude
    
    return np.sin(positives) 

sanityTime = np.array([np.datetime64('2018-06-21T00:00:00', 's'), np.datetime64('2019-06-21T00:00:00', 's')])
#sanityTime = np.array([np.datetime64('2018-12-22T12:00:00', 's'), np.datetime64('2019-12-22T12:00:00', 's')])
sanitySun = current.localSun(time = sanityTime, start = idealStart, day = day, year = year)
print("(2) For sanity check after 1 year, let's check the observers vectors.\n")
print(sanitySun.obsV())
print("\nThey are the same. So we're good. Let's also test a few random times so that they work:")

# Plot the starting point and end point.

startEnd = np.array([np.datetime64('2018-12-22T12:00:00', 's'), np.datetime64('2019-12-22T12:00:00', 's')])
startEndSun = current.localSun(time = startEnd)

fig2 = plt.figure()
ax2 = fig2.gca(projection='3d')
ax2.set_xlim3d(-1.5, 1.5)
ax2.set_ylim3d(-1.5, 1.5)
ax2.set_zlim3d(-1.5, 1.5)

for v in np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) :
    ax2.quiver(0, 0, 0, v[0], v[1], v[2], length = 0.5, normalize = False, color = 'k')

# Iterate through each vector. After that plot each
weirdCount = 0
I = 0

posEarths2 = current.earthDir(startEndSun.orientY)

for w in posEarths2:
    ax2.quiver(w[0], w[1], w[2] , startEndSun.tiltVec[0], startEndSun.tiltVec[1], startEndSun.tiltVec[2], length = 0.9 + +.5*weirdCount \
              , normalize = False, color = 'k')
    
    for K in np.arange(0,3):
        ax2.quiver(w[0], w[1], w[2], startEndSun.obsV()[K][I][0], startEndSun.obsV()[K][I][1], startEndSun.obsV()[K][I][2], \
                   length = 0.4 + weirdCount*0.3, normalize = False, color = '{:}'.format(colors[K]))
    I += 1
    weirdCount += 1

# For final sanity check plot a few random datetimes
J = 0
randomTests = np.array([np.datetime64('2019-02-22T18:00:00', 's'), np.datetime64('2019-01-19T14:34:00', 's'), \
                        np.datetime64('2019-06-22T12:00:00', 's'), np.datetime64('2019-04-22T00:00:00', 's'), \
                        np.datetime64('2019-09-22T21:00:00', 's'), np.datetime64('2019-11-22T22:00:00', 's')])

rndSuns = current.localSun(clat = 150, time = randomTests)
posEarths3 = current.earthDir(rndSuns.orientY)

for w in posEarths3:
    ax2.quiver(w[0], w[1], w[2] , rndSuns.tiltVec[0], rndSuns.tiltVec[1], rndSuns.tiltVec[2], length = 0.9 \
              , normalize = False, color = 'k')
    
    for K in np.arange(0,3):
        ax2.quiver(w[0], w[1], w[2], rndSuns.obsV()[K][J][0], rndSuns.obsV()[K][J][1], rndSuns.obsV()[K][J][2], \
                   length = 0.4, normalize = False, color = '{:}'.format(colors[K]))
    J += 1

# (3) Calculate heat vector

heatVector = np.zeros([181, 1])
i = 0


# Iterate through the 180 degrees latitude
for latitude in np.arange(0, 181):
    latSun = current.localSun(clat = latitude, time = oneYear, tilt = tilt, start = idealStart, day = day, year = year)
    
    heatVector[i] = sum(yearSun(latSun.altitude()))
    i += 1

fig3 = plt.figure('Heat distribution')
ax3 = fig3.gca()
ax3.plot(np.arange(0, 181), heatVector, lw = 2)
ax3.set(xlabel='Colatitude', ylabel='Power (arb. units)',
       title='Solar power over a year with {:.2f}$^\circ$ tilt'.format(math.degrees(tilt)))
ax3.grid()
ax3.set_ylim([0, max(heatVector)*1.1])
plt.show()

print("\nMaximum and minimum deviation from a symmetric array with {:.2f} tilt:".format(math.degrees(tilt)))
maxDev = max(heatVector - np.flip(heatVector))
minDev = min(abs((heatVector - np.flip(heatVector))))
print(maxDev, minDev)
signDeviation = (heatVector - np.flip(heatVector)) >= 1e-09
print("\nSum of ones: {:d}".format(sum(signDeviation)[0]))

print("\nThis is not a very small number. Something is wrong!")

fig4 = plt.figure('Anomaly')
ax4 = fig4.gca()
ax4.scatter(np.arange(0,181), signDeviation, s = 1)
plt.show()






