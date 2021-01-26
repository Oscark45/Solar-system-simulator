"""
Author:     Oscar Kaatranen
Created:    %(date)$
Modified:   %(date)$ 

Description

Ideal conditions:
1. Earth's orbit is perfectly circular.
2. Earth has 0 tilt.

This file is used to test the position of the Earth in ideal conditions.

"""
import numpy as np
import matplotlib.pyplot as plt
import localSun as current
import math as math
import random
import help_functions as hp
import itertools

plt.close('all')

day = 86400 - 86400/366
year = 31536000
idealStart = np.array([np.datetime64('2018-12-22T00:00:00', 's')])
tiltTest = math.radians(23.44) # Normal tilt

print("(1) Testing to see if the numbers are exact on the solstices and equinoxes. These numbers should be exact to arbitrary precision regardless of tilt.\n")

# Solstices and equinoxes
solsSun1 = current.localSun(time = np.array([np.datetime64('2018-12-22T00:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
solsSun2 = current.localSun(time = np.array([np.datetime64('2019-06-22T12:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
eqSunM = current.localSun(time = np.array([np.datetime64('2019-03-23T06:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
eqSunS = current.localSun(time = np.array([np.datetime64('2019-09-21T18:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)

testSuns = np.array([solsSun1, eqSunM, solsSun2, eqSunS])

fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D # This is apparently needed for the '3d' next line
ax = fig.gca(projection='3d')
ax.set_xlim3d(-1.7, 1.7)
ax.set_ylim3d(-1.7, 1.7)
ax.set_zlim3d(-1.7, 1.7)

# Plot the coordinate axes
for v in np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 0.5]]) :
    ax.quiver(0, 0, 0, v[0], v[1], v[2], length = 0.5, normalize = False, color = 'k')

# Plot the plane, position vector and tilt of Earth
for test in testSuns:
    posEarth = hp.earthDir(np.array([test.orientY]))*1.2
    x,y,z = test.radialV()
    print("Time: {}".format(test.time[0]))
    print("Sun colatitude: {}".format(np.degrees(test.latSun()[0])))
    print("Observer colatitude: {}".format(np.degrees(test.clat[0])))
    print("Sun altitude: {}\n".format(np.degrees(test.altitude()[0])))
    
    for orientation in np.linspace(0, 2*np.pi, num=20):
        earthVector = hp.planeV(np.array([orientation]))
        ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2], earthVector[0][0], earthVector[0][1], \
              earthVector[0][2], length = 0.25 , normalize = False, color = 'green')  
            
    ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2], \
        hp.tiltV(test.tilt)[0], hp.tiltV(test.tilt)[1], hp.tiltV(test.tilt)[2], length = 1.1 , normalize = False, color = 'k') 

    ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2], \
        x,y,z, length = 0.6 , normalize = False, color = 'r') 

# Plot the orbit
xs = np.cos(np.linspace(0, 2*np.pi, num = 200))*1.2
ys = np.sin(np.linspace(0, 2*np.pi, num = 200))*1.2
ax.scatter(xs,ys, marker = '.')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.text(1,0,1.3,'Winter Solstice')
ax.text(0,1,1.3,'Spring Equinox')
ax.text(-2,0,-0.8,'Summer Solstice')
ax.text(-0.2,-1,-0.8,'Autumn Equinox')
ax.grid(False)
plt.show()

print("(2) Let's test the some midday, midnight and sunset situations with 0 tilt. These should be exact regardless of latitude and day of year.\n")

# Add random days to the starting points.
midDays = np.array([np.datetime64('2019-12-22T12:00:00', 's') for i in range(6)]) \
+ sorted(np.array([random.randint(1, 365) for i in range(6)]) * 86400)

midNights = np.array([np.datetime64('2019-12-22T00:00:00', 's') for i in range(6)]) \
+ sorted(np.array([random.randint(1, 365) for i in range(6)]) * 86400)

sunRises = np.array([np.datetime64('2019-12-22T06:00:00', 's') for i in range(6)]) \
+ sorted(np.array([random.randint(1, 365) for i in range(6)]) * 86400)

sunSets = np.array([np.datetime64('2019-12-22T18:00:00', 's') for i in range(6)]) \
+ sorted(np.array([random.randint(1, 365) for i in range(6)]) * 86400)

# Random latitudes
latitudes = np.array([random.randint(0,180) for i in range(4)])

midDaySun = current.localSun(clat = latitudes[0], time = midDays, tilt = 0, day = day, year = year, start = idealStart)
midNightSun = current.localSun(clat = latitudes[1], time = midNights, tilt = 0, day = day, year = year, start = idealStart)
sunRiseSun = current.localSun(clat = latitudes[2], time = sunRises, tilt = 0, day = day, year = year, start = idealStart)
sunSetSun = current.localSun(clat = latitudes[3], time = sunSets, tilt = 0, day = day, year = year, start = idealStart)

print("Midday altitude angles at colatitude {:d}: \n{}\n".format(latitudes[0], np.degrees(midDaySun.altitude())))
print("Midnight altitude angles at colatitude {:d}: \n{}\n".format(latitudes[1], np.degrees(midNightSun.altitude())))
print("Sunrise altitude angles at colatitude {:d}: \n{}\n".format(latitudes[2], np.degrees(sunRiseSun.altitude())))
print("Sunset altitude angles at colatitude {:d}: \n{}\n".format(latitudes[3], np.degrees(sunSetSun.altitude())))
print("\nThese are all very close to exact. Good job!\n")


print("(3) Let's test the summer solstice middays for all the colatitudes")
clats = np.arange(0,181,1)
lon = np.zeros(181)

midDayAllS = current.localSun(clat = clats, lon = lon ,\
    time = np.array([np.datetime64('2019-06-22T12:00:00', 's')]), tilt = tiltTest,\
    day = day, year = year, start = idealStart)
midNightAllW = current.localSun(clat = clats, lon = lon ,\
    time = np.array([np.datetime64('2018-12-22T00:00:00', 's')]), tilt = tiltTest,\
    day = day, year = year, start = idealStart)

midDayS = current.localSun(clat = clats, lon = lon ,\
    time = np.array([np.datetime64('2019-03-22T12:00:00', 's')]), tilt = tiltTest,\
    day = day, year = year, start = idealStart)
        
midDayA = current.localSun(clat = clats, lon = lon ,\
    time = np.array([np.datetime64('2019-09-22T12:00:00', 's')]), tilt = tiltTest,\
    day = day, year = year, start = idealStart)
    
# If you print these, they should give correct results
altsS = np.degrees(midDayAllS.altitude())
altsW = np.degrees(midNightAllW.altitude())
altsEqS = np.degrees(midDayS.altitude())
altsEqA = np.degrees(midDayA.altitude())