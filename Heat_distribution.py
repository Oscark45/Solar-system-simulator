import numpy as np
import matplotlib.pyplot as plt
import localSun as current
import math as math
from scipy.integrate import simps
import os

# Given an array of altitudes, take only those into account that are > 0
def heat(altitude, r):    
    positives = altitude * (altitude > 0)*1     
    return positives/r**2 

def gaussHeat(i, array):
    return array[i]

day = 86400 - 86400/366
year = 31536000
idealStart = np.array([np.datetime64('2018-12-22T00:00:00', 's')])
perihelion0 = idealStart
oneYear =  np.arange('2018-12-22T00:00:00', '2019-12-22T00:00:00', dtype = 'datetime64[60m]')

clats = np.array([np.arange(0,180+1)])
lon = np.array([np.zeros(len(clats[0]))])

tilts = np.array([23.44])
#tilts = np.array([0, 11, 23.44, 23.44*2, 90])
#tilts = np.array([23.44, 23.44*2])

eccs = np.array([0.0167])
#eccs = np.array([0, 0.0167, 0.0934, 0.2056, 0.5])

fig = plt.figure('Heat distribution')
ax = fig.gca()
maxValue = 0

for tilt in tilts:
    for ecc in eccs:
        yearSun = current.localSun(clat = clats, lon = lon, time = oneYear, tilt = math.radians(tilt), \
                start = idealStart, day = day, year = year, ecc = ecc, perihelion = perihelion0)
        # Comment/uncomment these if you want to calculate with different method
        #heatVector = np.sum(heat(yearSun.altitude(False), yearSun.radii), axis = 1)
        #heatVector = np.trapz(heat(yearSun.altitude(siny = False), yearSun.radii), axis = 1)
        #heatVector = simps(heat(yearSun.altitude(siny = False), yearSun.radii), axis = 1)
        heatVector = np.loadtxt(os.getcwd() + "\\value_{:.2f}_{:.4f}.txt"\
                               .format(np.degrees(yearSun.tilt), yearSun.ecc))
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        ax.plot(np.arange(0, 181), heatVector*60, lw = 2, \
            label = '{:.2f}$^\circ$, $\epsilon={}$'.format(tilt, ecc))
            #label = '$\epsilon={}$'.format(ecc))
            #label = '{:.2f}$^\circ$'.format(tilt))
        maxValue = max(maxValue, max(heatVector*60))

plt.xlabel('Colatitude $\phi$', fontsize = 16)
plt.ylabel('Solar irradiance (arb. units)', fontsize = 16)
#plt.title(r"Varying eccentricity ($\alpha=${})".format(tilt), fontsize = 16)
#plt.title(r'Varying tilt ($\epsilon=${})'.format(ecc), fontsize = 16)
#plt.title(r'Comparison of various $\alpha$ and $\epsilon$', fontsize = 16)
plt.title(r'Unphysical, constant angular speed ($\alpha$={})'.format(tilt), fontsize = 16)
#ax.grid()
ax.set_ylim([0, maxValue*1.1])
ax.set_xlim([0,180])
ax.set_xticks(np.arange(0,180+30, step = 30))
ax.tick_params(labelsize=16)
plt.legend(prop={'size': 12})
plt.show()