# -*- coding: utf-8 -*-
"""
Created on Wed May 27 19:29:25 2020

@author: Oscar
"""

"""
The idea is to calculate the heatVector with the adaptive trapezoidal rule
and save the results in a text file. These calculations, unlike RK4 is not properly 
optimized. For some reason my IDE (Spyder) started acting really slowly and
crashed at times hence a loop to calculate for all the wanted tilt and ecc values
did not seem feasible. I did it manually by changing the parameters of testSun
It took time but managed to eventually do without problems
"""

import numpy as np
import matplotlib.pyplot as plt
import math as math
import os
import Adaptive_trapz as AT
import localSun as current
import scipy.integrate as scint

# Change these if you want to calculate or plot
calculate = False
plotError = False
plotN = False

# Given an array of altitudes, take only those into account that are > 0
def heat(altitude, r):    
    positives = altitude * (altitude > 0)*1     
    return positives/r**2 

day = 86400 - 86400/366
year = 31536000
idealStart = np.array([np.datetime64('2018-12-22T00:00:00', 's')])
perihelion0 = idealStart
tilt = 23.44
# Change dtype = 'datetime64[1m]' for each minute
oneYear =  np.arange('2018-12-22T00:00:00', '2019-12-22T00:00:00', dtype = 'datetime64[60m]')
N = len(oneYear)
ecc = 0.0167

clats = np.array([np.arange(0,180+1)])
lon = np.array([np.zeros(len(clats[0]))])

testSun = current.localSun(clat = clats, lon = lon, time = oneYear, tilt = math.radians(tilt), \
            start = idealStart, day = day, year = year, ecc = ecc, perihelion = perihelion0)

heatTest = heat(testSun.altitude(False), testSun.radii)

testAlt = testSun.altitude(False)
radii = testSun.radii
timeIdx = testSun.dt

if calculate:
    def gaussHeat(i, index = 0):
        return heatTest[index, i]

    heatAdapt = np.zeros(181)
    n_values = np.zeros(181)
    for i in range(181):
        value, n = AT.adaptive_integration(gaussHeat, 0, N-1, 1e-03, i)
        value = value*60
        heatAdapt[i] =  value
        n_values[i] = n
        print(n,i)

    np.savetxt(os.getcwd() + "\\value_{:.2f}_{:.4f}.txt".format(tilt, ecc), heatAdapt,
               delimiter = ' ', newline = '\n', fmt = '%4.13f')
    
    np.savetxt(os.getcwd() + "\\n_value_{:.2f}_{:.4f}.txt".format(tilt, ecc), n_values,
               delimiter = ' ', newline = '\n', fmt = '%d')
else:
    heatAdapt = np.loadtxt(os.getcwd() + "\\value_{:.2f}_{:.4f}.txt".format(tilt, ecc))

'''
Results obtained with:
    1) Midpoint rule (basic rectangular Riemann sum)
    2) Trapezoidal rule
    3) Simpsons rule
'''
heatRect = np.sum(heat(testAlt, radii)*60, axis = 1)
heatTrap = np.trapz(heat(testAlt, radii), timeIdx, axis = 1)
heatSimps = scint.simps(heat(testAlt, radii), timeIdx, axis = 1)

if plotError:    
    fig = plt.figure()
    ax = plt.gca()
    plt.plot((heatTrap - heatSimps)/heatSimps, label = 'Trapezoidal')
    plt.plot((heatAdapt - heatSimps)/heatSimps, label = 'Adaptive trapezoidal')
    plt.plot((heatRect-heatSimps)/heatSimps, label = 'Rectangular')
    plt.title(r'Relative error compared to Simpsons rule ($\alpha=$, $\epsilon={}$)'.format(tilt, ecc), fontsize = 16)
    plt.xlabel(r'Colatitude $\phi$', fontsize = 16)
    plt.ylabel('Relative error', fontsize = 16)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    ax.set_xticks(np.arange(0,180+30, step = 30))
    ax.tick_params(labelsize=16)
    plt.legend()
    plt.show()
    
# Plot the amount of n needed for trapezoidal integration
if plotN:
    fig = plt.figure()
    ax = plt.gca()
    n = np.loadtxt(os.getcwd() + "\\n_value_{:.2f}_{:.4f}.txt".format(tilt, ecc))
    plt.plot(np.linspace(1,181,181), abs(n))
    plt.xlabel(r'Colatitude $\phi$', fontsize = 16)
    plt.ylabel('Amount', fontsize = 16)
    plt.title(r'Adaptive integration points ($\alpha$={},$\epsilon$={})'.format(tilt, ecc), fontsize = 16)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    ax.tick_params(labelsize=16)
    ax.set_xticks(np.arange(0,180+30, step = 30))
    
    