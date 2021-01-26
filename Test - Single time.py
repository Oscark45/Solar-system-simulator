# -*- coding: utf-8 -*-
"""
Created on Sun May 24 10:51:18 2020

@author: Oscar
"""

# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

"""
Author:     Oscar Kaatranen
Created:    % 11/08/2019 $
Modified:   % (date) $ 

Description

Make an arbitrary one sun test.

"""

import numpy as np
import matplotlib.pyplot as plt
import localSun as current
from datetime import datetime
import math as math
import help_functions as hp
import Adaptive_Simpson as AS

clat0 = np.array([30])
lon0 = np.array([0])
tilt0 = math.radians(23.43693) # Obvious
time0 = np.array([np.datetime64('2019-06-22T00:00:00', 's')]) # 2019 Winter Solstice (UTC)
#start0 = np.datetime64('2019-12-22T04:19:00', 's') # 2019 Winter Solstice (UTC)
start0 = np.array([np.datetime64('2018-12-22T00:00:00', 's')]) # 2019 Winter Solstice (UTC)
day0 = 23*3600 + 56*60 + 4.0905 # Sidereal day
year0 = 365*86400 + 6*3600 + 9*60 + 9.76 # Sidereal year
perihelion0 = np.array([np.datetime64('2019-03-21T00:00:00', 's')]) # 2020 perihelion (UTC)
perihelion0 = start0


# Perfect year and perfect day
day = 86400 - 86400/366
year = 31536000

testSun = current.localSun(clat = clat0, lon = lon0, time = time0, tilt = tilt0, \
                           start = start0, day = day0, year = year0, ecc = 0.3, \
                               perihelion = perihelion0, units = "minutes")

oneYear =  np.arange('2018-12-22T00:00:00', '2019-12-22T00:00:00', dtype = 'datetime64[1m]')
yearSun = current.localSun(clat = clat0, lon = lon0, time = oneYear, tilt = tilt0, \
                           start = start0, day = day0, year = year0, ecc = 0.6, \
                               perihelion = perihelion0, units = "minutes")
    

angle = yearSun.angleY
e1 = yearSun.ecc    

x_values = np.cos(angle)*yearSun.radii
y_values = np.sin(angle)*yearSun.radii
    
fig = plt.figure()
ax = fig.gca()
ax.axis('equal')
plt.plot(x_values, y_values)
#plt.polar(angle, hp.polarEllipse(angle, e1, advance = yearSun.advance))
#plt.polar(angle, yearSun.radii)

def heat(i):
    if type(i) == float:
        i = int(i)
    positive = yearSun.altitude()[i]*(yearSun.altitude()[i] >= 0) * 1

    return positive/yearSun.radii[i]**2

a = AS.quad_asr(heat, 50000, 50010, 0.5)

    