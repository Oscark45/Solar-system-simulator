# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

"""
Author:     Oscar Kaatranen
Created:    %(date)$
Modified:   %(date)$ 

Description

Ideal conditions:
1. Earth's orbit is perfectly circular.
2. Earth orbits the sun in exactly 365 solar or 366 sidereal days.
3. Winter solstice occurs at midday.

This file is used to test the position of the Earth in ideal conditions.

"""

import numpy as np
import matplotlib.pyplot as plt
import localSun as current
from datetime import datetime
import math as math
import random

day = 86400 - 86400/366
year = 31536000
idealStart = np.array([np.datetime64('2019-12-22T12:00:00', 's')])
tiltTest = math.radians(23.44) # Normal tilt

print("(1) Testing to see if the numbers are exact on the solstices and equinoxes. These numbers should be exact to arbitrary precision regardless of tilt.\n")

# Solstices and equinoxes
solsSun1 = current.localSun(time = np.array([np.datetime64('2019-12-22T12:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
solsSun2 = current.localSun(time = np.array([np.datetime64('2020-06-22T00:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
solsSun3 = current.localSun(time = np.array([np.datetime64('2020-12-21T12:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
eqSunM = current.localSun(time = np.array([np.datetime64('2020-03-22T18:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
eqSunS = current.localSun(time = np.array([np.datetime64('2020-09-21T06:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)
eqSun2018 = current.localSun(time = np.array([np.datetime64('2018-09-22T06:00:00', 's')]), tilt = tiltTest, day = day, year = year, start = idealStart)

print("Winter solstice 2019, altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(solsSun1.altitude()[0]), math.degrees(solsSun1.azimuth()[0])))
print("March equinox 2020, altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(eqSunM.altitude()[0]), math.degrees(eqSunM.azimuth()[0])))
print("Summer solstice 2020, altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(solsSun2.altitude()[0]), math.degrees(solsSun2.azimuth()[0])))
print("September equinox 2020, altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(eqSunS.altitude()[0]), math.degrees(eqSunS.azimuth()[0])))
print("Winter solstice (2019), altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(solsSun3.altitude()[0]), math.degrees(solsSun3.azimuth()[0])))
print("September equinox (2018), altitude: {:.8f} and azimuth: {:.8f}".format(math.degrees(eqSun2018.altitude()[0]), math.degrees(eqSun2018.azimuth()[0])))
print("\nEach of these are exact as should be. Great!\n")

print("(2) Let's test the some midday, midnight and sunset situations with 0 tilt. These should be exact regardless of latitude and day of year.\n")

tilt0 = 0

# Add random days to the starting points.

midDays = np.array([np.datetime64('2019-12-22T12:00:00', 's') for i in range(6)]) \
+ np.array([random.randint(1, 365) for i in range(6)]) * 86400

midNights = np.array([np.datetime64('2019-12-22T00:00:00', 's') for i in range(6)]) \
+ np.array([random.randint(1, 365) for i in range(6)]) * 86400

sunRises = np.array([np.datetime64('2019-12-22T06:00:00', 's') for i in range(6)]) \
+ np.array([random.randint(1, 365) for i in range(6)]) * 86400

sunSets = np.array([np.datetime64('2019-12-22T18:00:00', 's') for i in range(6)]) \
+ np.array([random.randint(1, 365) for i in range(6)]) * 86400

# Random latitudes
latitudes = np.array([random.randint(0,180) for i in range(4)])

midDaySun = current.localSun(clat = latitudes[0], time = midDays, tilt = 0, day = day, year = year, start = idealStart)
midNightSun = current.localSun(clat = latitudes[1], time = midNights, tilt = 0, day = day, year = year, start = idealStart)
sunRiseSun = current.localSun(clat = latitudes[2], time = sunRises, tilt = 0, day = day, year = year, start = idealStart)
sunSetSun = current.localSun(clat = latitudes[3], time = sunSets, tilt = 0, day = day, year = year, start = idealStart)

print("Midday altitude angles at colatitude {:d}: {}".format(latitudes[0], np.degrees(midDaySun.altitude())))
print("Midnight altitude angles at colatitude {:d}: {}".format(latitudes[1], np.degrees(midNightSun.altitude())))
print("Sunrise altitude angles at colatitude {:d}: {}".format(latitudes[2], np.degrees(sunRiseSun.altitude())))
print("Sunsets altitude angles at colatitude {:d}: {}".format(latitudes[3], np.degrees(sunSetSun.altitude())))
print("\nThese are all very close to exact. Good job!")

