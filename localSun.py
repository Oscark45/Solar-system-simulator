# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

"""
Author:     Oscar Kaatranen
Created:    %(date)$
Modified:   %(date)$ 

Description

"""

import numpy as np
import matplotlib.pyplot as plt
import math as math
from datetime import datetime
import os
import help_functions as hp
from RK4 import ellipticalOrbit

""" STARTS AT THE WINTER SOLSTICE FOR NORTHERN HEMISPHERE """
clat0 = np.array([30])
lon0 = np.array([0])
tilt0 = math.radians(23.43693) # Obvious
time0 = np.array([[datetime.now()]], dtype = 'datetime64[s]')
#start0 = np.datetime64('2019-12-22T04:19:00', 's') # 2019 Winter Solstice (UTC)
start0 = np.array([np.datetime64('2019-12-22T00:00:00', 's')]) # 2019 Winter Solstice (UTC)
day0 = 23*3600 + 56*60 + 4.0905 # Sidereal day
year0 = 365*86400 + 6*3600 + 9*60 + 9.76 # Sidereal year
perihelion0 = np.array([np.datetime64('2020-01-05T07:48:00', 's')]) # 2020 perihelion (UTC)

# Perfect year and perfect day
day = 86400 - 86400/366
year = 31536000

""" THE CLASS localSun """

timeDict = {"seconds": 1, "minutes": 60, "hours": 3600}

class localSun:
    
    """ The local Sun class is used to compute various properties of how the sun behaves \
    in a geocentric picture. Such as altitude now at your location. Altitude at noon any time,
    anywhere, length of day etc. If no time is given, it evaluates the time now"""
    
    def __init__(self, clat=clat0, lon=lon0, time = time0, tilt = tilt0, start = start0, \
                 day = day0, year = year0, ecc = 0, perihelion = perihelion0, units = "minutes"):
        
        # Parameters
        self.clat = np.radians(clat) # Colatitude(s) of observer.
        self.lon = np.radians(lon) # Longitude(s) of observer.
        self.time = time # Datetime objects.
        self.tilt = tilt # Axial tilt. Normally 23.44 degrees (0.409 radians).
        self.start = start # Starting time.
        self.day = day # Duration of sidereal day.
        self.year = year # Duration of solar year.
        self.ecc = ecc # Eccentricity.
        self.perihelion = perihelion if ecc !=0 else start # Perihelion time
        # If eccentricity is 0, then might as well just put perihelion to be the solstice
        
        # Calculated quantities
        self.dt = (time-start)/np.timedelta64(1,'s') # Time difference in seconds
        self.dtSols = (time - start)/np.timedelta64(1, 's') # Time difference from solstice
        self.orientY = self.dt%self.year/self.year*2*np.pi # Year orientation circle
        self.orientD = self.dt%self.day/self.day*2*np.pi # Day orientation.     
                
        self.perihelion = perihelion
        self.dtPer = (self.perihelion - self.start)/np.timedelta64(1, 's') # Time difference from perihelion
        self.advance = ellipticalOrbit(self.ecc, self.dtPer/self.year*2*np.pi)[1]
        
        # Default offset angle measured from the chosen midday.
        midStart = np.datetime64('2018-12-22T12:00:00', 's')
        self.yearDefault = (self.start- midStart)/np.timedelta64(1, 's')*2*np.pi/self.year # Default year orientation
        self.default = (self.start - midStart)/np.timedelta64(1,'s')/self.day * 2*np.pi - self.yearDefault
        
        def read_orient(): # Reads the orientations and returns the indices
            
            if len(time) == 1: # If just one time, calculate simply without wasting time.
                return ellipticalOrbit(self.ecc, self.dt/self.year * 2*np.pi)[1]
            
            if len(time) == 8760:
                angles = ellipticalOrbit(self.ecc, self.dt/self.year * 2*np.pi).flatten()
                return angles
        
            if len(time) == 525600:
                fileName = "ecc{:.4f}.txt".format(self.ecc)
                angles = np.loadtxt(os.getcwd() + "\\Eccentricities2\\" + fileName)
                return angles[:-1]
            return angles
            
        self.timeIdx = self.dt # Time indices. For example 27660 is the 461th minute
        self.angleY = (self.orientY if self.ecc == 0 else read_orient())
        self.radii = hp.polarEllipse(self.angleY, self.ecc, advance = self.advance)

    def radialV(self, g):
        
        clatC = self.clat.transpose()
        x = np.array(np.cos(self.tilt)*np.sin(clatC)*np.cos(self.orientD) \
                      + np.sin(self.tilt)*np.cos(clatC))
        y = np.array(np.sin(self.orientD)*np.sin(clatC))
        z = np.array(-np.sin(self.tilt)*np.sin(clatC)*np.cos(self.orientD) \
                      + np.cos(self.tilt)*np.cos(clatC))
            
        return x,y,z
    
    def altitude(self, siny = True):
            
        clatC = self.clat.transpose()
        #orientY = self.angleY
        orientY = self.orientY
        dotP = - np.cos(self.tilt)*np.cos(orientY)*np.cos(self.orientD)*np.sin(clatC) \
            - np.sin(self.tilt)*np.cos(orientY)*np.cos(clatC) \
            - np.sin(orientY)*np.sin(self.orientD)*np.sin(clatC)  
            
        # Due to floating points numbers, some values of siny are like 1.000001
        # Change these to 1 to avoid issues with arcsin() function
        dotP = dotP * (abs(dotP) <= 1) + 1*(abs(dotP) > 1)*np.sign(dotP)
        
        # If siny is True, return the actual angle, otherwise return just siny
        # The idea is to reduce the amount of unnecessary sin(arcsin(...))
        # calls which might cause inaccuracies due to floating point numbers
        
        if siny:
            return np.arcsin(dotP)
        else:
            return dotP
        
    def latSun(self):
        return np.arccos(-np.sin(self.tilt)*np.cos(self.angleY))