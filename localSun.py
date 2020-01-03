# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

"""
Author:     Oscar Kaatranen
 
Description

This is the main file for the simulator. The class parameters given to the localSun class specify the length of year, day, tilt angle etc. 
Default parameters are the real parameters for Earth.

"""

import numpy as np
import matplotlib.pyplot as plt
import math as math
from datetime import datetime
from scipy.integrate import odeint

""" STARTS AT THE WINTER SOLSTICE FOR NORTHERN HEMISPHERE (2019) """

clat0 = 30
lon0 = 0
tilt0 = math.radians(23.43693) # Obvious
time0 = np.array([datetime.now()], dtype = 'datetime64[s]')
start0 = np.datetime64('2019-12-22T04:19:00', 's') # 2019 Winter Solstice
day0 = 23*3600 + 56*60 + 4.0905 # Sidereal day
year0 = 365*86400 + 6*3600 + 9*60 + 9.76 # Sidereal year

# Perfect year and perfect day
#day = 86400 - 86400/366
#year = 31536000

""" UNIT VECTORS IN SPHERICAL COORDINATES """ # colatitude used 

def unitR(clat, lon): # Radial unit vector
    
    r = np.array([np.sin(clat)*np.cos(lon) 
                      , np.sin(clat)*np.sin(lon)
                      , np.cos(clat)])
    # unitR(np.array([np.pi/2,np.pi,np.pi*3/2,2*np.pi]),np.array([0,0,0,0])) WORKS
    return r

def unitP(clat, lon): # Polar unit vector
    
    o = np.array([np.cos(clat)*np.cos(lon) 
        , np.cos(clat)*np.sin(lon)
        , -np.sin(clat)])
    
    return o

def unitA(clat, lon): # Azimuthal unit vector
    
    # Should work when reshaped properly, dimensions are wrong if for many
    
    return np.cross(unitR(clat, lon), unitP(clat, lon)) # Simple with cross product
    # Normally np.array([-np.sin(lon), np.cos(lon), 0]) 


""" VECTORS RELEVANT TO THE SUN-EARTH SYSTEM """

def tiltV(phi = tilt0): # Tilt vector at the winter solstice. Points in positive x direction with y=0.
    return np.array([np.sin(phi), 0, np.cos(phi)])
    
def rodV(v, theta, k = tiltV()): # Rodrigues rotation formula. Default rotation around the tilt
    
    # v = np.array([[1,2,3],[4,5,6], [7,8,9], [10, 11, 12], [13, 14, 15]])
    # k = np.array([1,2,3])
    # theta = np.array([0,1,2,3,4]).reshape(-1,1)
    
    theeta = theta.reshape(-1,1) # Makes theta into a single column vector (transposes). Is necessary
    
    v1 = v*np.cos(theeta) # First term.
    v2 = np.cross(k,v)*np.sin(theeta) # Second term 
    v3 = k*np.dot(v,k).reshape(-1,1)*(1-np.cos(theeta)) # Third term

    return v1+v2+v3 # Return their sum as is on the Wikipedia page.

def planeV(theta, phi=tilt0): # The plane of Earth's equator
    
    # theta = how much rotate.
    # Initially the vector points towards the sun on the winter solstice.
    # Rotates around the tilt vector i.e the Earth's axis.
    
    planeInit = np.array([[-np.cos(phi)]*len(theta), [0]*len(theta), [np.sin(phi)]*len(theta)]).transpose()
    
    return rodV(planeInit, theta, k = tiltV(phi))

def planeV2(theta, phi=tilt0): # The plane of Earth's equator
    
    # theta = how much rotate.
    # Initially the vector points towards the sun on the winter solstice.
    # Rotates around the tilt vector i.e the Earth's axis.
    
    planeInit = np.array([[-np.cos(phi)]*len(theta), [0]*len(theta), [np.sin(phi)]*len(theta)]).transpose()
    
    return planeInit

def earthDir(theta): # Direction of the Earth poiting from the Sun
    
    # This vector lies of the xy-plane so z=0.
    
    return np.array([np.cos(theta), np.sin(theta), np.zeros(len(theta))]).transpose()

def sunV(theta): # Direction of the Sun pointing from the Earth (opposite of earthDir)
    return -earthDir(theta)

def angleV(u, v):
    return np.arccos(np.dot(u,v)/(np.linalg.norm(u) * np.linalg.norm(v)))


"""
Other useful functions.
"""

def angleVectors(M,V): # Calculates the dot product between corresponding vectors. M and V can both be matrices
                 # M and V must have unit vectors, otherwise it will mess up the result
    # Apparently sum() is a fast function that is built with C
    
    massiveProduct = sum((M*V).transpose())
    
    # This just turns all values above 1 to ones (or minus ones if negative). 
    # This is a problem that occurs due to floating point numbers
    absVal = np.abs(massiveProduct)
    massiveProduct = (massiveProduct * (absVal <= 1) + 1*(absVal > 1)*np.sign(massiveProduct))
    
    return np.arccos(massiveProduct)

def dotVectors(M,V):
    return sum((M*V).transpose())
                 
""" THE CLASS localSun """

"""
Takes eccentricity, duration, initial orientation and final orientation
and returns the array of radii and angles.
"""

def ellipticalOrbit(e, duration, theta0 = 0, thetaF = 2*np.pi):
    
    """ 
    Parameters:
    e: eccentricity
    duration: duration in some units (seconds, minutes, hours or what ever)
    theta0: initial angle, normally 0
    thetaF: final angle, normally 2*pi
    
    With this setup and normalized units the time of one orbit is T=2*pi 
    """
    
    # Helper functions. Both assume semi-major axis 1.
    def planetFunction(theta, time, e): # Differential equation for elliptical orbit
        return (1 + e * np.cos(theta))**2 / (1 - e**2)**(3/2)
    def polarEllipse(theta, e): # Polar equation of an ellipse
        return (1-e**2)/(1+e*np.cos(theta))
        
    # The total angle vector from theta0 to thetaF. Default 0 to 2*pi with duration amount of entries
    timeVector = np.linspace(theta0, thetaF, int(duration)) # Time steps
    angle = odeint(planetFunction, theta0, timeVector, args = (e,)) # Final angle vector
    radii = polarEllipse(angle, e) # Radial components
    
    return np.array([radii, angle]) # (If you want, you can return tuple (radii, angle))

def ellipticalOrbitArb(e, timeVector, theta0 = 0):
    
    """ 
    Parameters:
    e: eccentricity
    timeVector: an array of times to be used, normalize to [0, 2*pi]
    
    With this setup and normalized units the time of one orbit is T=2*pi 
    """
    
    # Helper functions. Both assume semi-major axis 1.
    def planetFunction(theta, time,  e): # Differential equation for elliptical orbit
        return (1 + e * np.cos(theta))**2 / (1 - e**2)**(3/2)
    def polarEllipse(theta, e): # Polar equation of an ellipse
        return (1-e**2)/(1+e*np.cos(theta))
        
    if len(timeVector) == 1: # If length is zero, add a zero to the beginning
        timeVector = np.insert(timeVector, 0, 0)

    angle = odeint(planetFunction, theta0, timeVector, args = (e,)) # Final angle vector
    radii = polarEllipse(angle, e) # Radial components
    
    return np.array([radii, angle]) # (If you want, you can return tuple (radii, angle))

timeDict = {"seconds": 1, "minutes": 60, "hours": 3600}

class localSun:
    
    """ The local Sun class is used to compute various properties of how the sun behaves \
    in a geocentric picture. Such as altitude now at your location. Altitude at noon any time,
    anywhere, length of day etc. If no time is given, it evaluates the time now"""
    
    def __init__(self, clat=clat0, lon=lon0, time = time0, tilt = tilt0, start = start0, \
                 day = day0, year = year0, ecc = 0, units = "minutes"):
        
        
        # np.arange('2005-02-01', '2005-02-02', dtype='datetime64[h]'), Lots of datetime objects, fast too
        # /np.timedelta64(1,'s') # Tällä tavalla voin saada arrayn jossa vaan lukuja datetime objektien sijaan
        
        # With normal settings we give colatitude 30, longtitude 0, the current time (single element in array),
        # and normal tilt of 23.44 degrees.
        
        # Parameters
        self.clat = math.radians(clat) # Colatitude of observer.
        self.lon = math.radians(lon) # Longitude of observer.
        self.time = time # Datetime objects.
        self.tilt = tilt # Axial tilt. Normally 23.44 degrees (0.409 radians).
        self.start = start # Starting time.
        self.day = day # Duration of sidereal day.
        self.year = year # Duration of solar year.
        self.ecc = ecc # Eccentricity.
        
        
        # Calculated quantities
        self.dt = (time-start)/np.timedelta64(1,'s') # Time difference in seconds
        self.tiltVec = tiltV(tilt) 
        self.orientD = self.dt%self.day/self.day*2*np.pi # Day orientation.
        # CHANGE orientY WHEN ELLIPTICAL ORBIT. NOW IT'S A SIMPLE CIRCLE.
        
        #ellipticalPar = ellipticalOrbit(self.ecc, )
        timeIdx = self.dt/timeDict[units] # Time indices. For example 27660 is the 461th minute
        self.orientY = self.dt%self.year/self.year*2*np.pi # Year orientation.
        
        # Default offset angle measured from the chosen midday.
        midStart = np.datetime64('2018-12-22T12:00:00', 's')
        self.yearDefault = (self.start- midStart)/np.timedelta64(1, 's')*2*np.pi/self.year # Default year orientation
        self.default = (self.start - midStart)/np.timedelta64(1,'s')/self.day * 2*np.pi - self.yearDefault
           
        """
        Directional vectors with the Sun-Earth system
        """
        self.sunV = sunV(self.orientY) # Direction of the Earth along the xy-plane  
      
    """
    Methods that were initially in the __init__ function
    """    
    
    """
    Normal methods
    """
    def obsV(self):
        # Observers vectors with [Radial, Polar, Azimuthal]. This is an array with 3 arrays.
        
        # Bunch of ones, a 3 dimensional vector corresponding to each time
        Ones = np.ones([len(self.time), 3])
        
        # Three steps for radial and polar vector:
        # 1. Create many unit vectors at this colatitude pointing at the x-axis.
        # 2. Rotate by taking into account longitude and the default offset.
        # 3. Map the radial vectors to match position at their times.
        # Could be done perhaps more succintly but optimization later
        
        """
        Radial unit vector
        """
        
        # Initial with tilt vector.
        # Longitude has to be 0 so that clat=0 gives the tilt vector (longitude indeterminate)
        r00 = unitR(self.clat + self.tilt, 0)*Ones
        
        # Take into account the longitude and orientation at the winter solstice.
        # Additional rotation of np.pi (180  degrees) is needed because 'default' is counted from midday.
        # The parameter 'default' is the offset angle from the moment of the solstice.
        r0 = rodV(r00, np.array([self.lon + np.pi + self.default]), self.tiltVec)
        
        # Rotate to the correct orientation at this moment.
        radial = rodV(r0, np.array([self.orientD]), self.tiltVec) 
        """
        Polar unit vector
        """
        
        # Same thing with the polar vector as with the radial vector.
        p00 = unitP(self.clat + self.tilt, 0)*Ones
        
        p0 = rodV(p00, np.array([self.lon + np.pi + self.default]), self.tiltVec)
        
        polar = rodV(p0, np.array([self.orientD]), self.tiltVec)
        
        """
        Azimuthal unit vector
        """
        
        # Simply use the cross product function.
        azimuthal = np.cross(radial, polar)
        
        return np.array([radial, polar, azimuthal])
    
    # Functions just to get the individual vectors, radial, polar and azimuthal
    
    def radialV(self): # Observers radial vectors
        return self.obsV()[0]
    
    def polarV(self): # Observers polar vectors
        return self.obsV()[1]
    
    def azimuthalV(self): # Observers azimuthal vectors
        return self.obsV()[2]
    
    def latSun(self): # The colatitude at which the Sun is directly above. 
        
        # Simple, just calculate the angle between the sun vector and tilt vector
        return np.arccos(np.dot(self.sunV, self.tiltVec))
    
        # Here's an old method. Doesn't work after all because planeE is incorrectly oriented!
        """
        return np.pi/2 + \
        np.arccos(sum((self.planeE*self.sunV).transpose())) * np.sign(self.planeE[:,2])
        
        # Idea is to calculate the dot product between planeV and sunV and
        # either add or subtract depending if the sun is north or south respectively
        # planeV[:,2] refers to the z-component which tells whether to add or subtract.
        """
    
    def altitude(self): 
        
        # Angle between each radial vector and sun vector.
        # For convenience (for now) it's the altitude from the horizon.
                        
        return np.pi/2 - angleVectors(self.obsV()[0], self.sunV) # WORKS (probably) 

    def azSun(self): # Helper function for azimuth and useful later. 
        # Returns a unit vector on the observers plane, gives the azimuthal direction of the sun.
        
        r = self.obsV()[0] # Radial unit vectors.
        
        u = self.sunV - sum((r * self.sunV).transpose()).reshape(-1,1)*r # Rejection vector
        
        # What this means for a single vector is the following: 
        # u = self.sunV - np.dot(r, self.sunV)*r
        # reshape(-1,1) transposes. This seems to be necessary
        
        # Compute the individual lengths because we need to return unit vectors
        uLengths = np.sqrt(sum((u*u).transpose())).reshape(-1,1)

        return u/uLengths
    
    def azimuth(self): # Return sun angle. Positive direction north-east-south-west
            
        dthetaPol = angleVectors(self.obsV()[1], self.azSun()) # Angle differential with polar
        dthetaAz = angleVectors(self.obsV()[2], self.azSun()) # Angle differential with azimuthal

        direction = np.pi + dthetaPol*np.sign(dthetaAz - np.pi/2)
        """
        North corresponds to 0. So from self.polarV() (+ np.pi)
        add the angle from polarV if the angle from azimuthV exceeds 90 degrees,
        otherwise subtract.
        """
        
        return direction    
        
