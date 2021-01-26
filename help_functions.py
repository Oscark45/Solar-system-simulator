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
import math as math

tilt0 = math.radians(23.43693) # Obvious

# Polar equation of an ellipse
def polarEllipse(theta, e, advance = 0):
    
    return (1-e**2)/(1+e*np.cos(theta - advance))

# Direction of the Earth poiting from the Sun
def earthDir(theta, r=1): 
    
    # This vector lies of the xy-plane so z=0.
    
    return r * np.array([np.cos(theta), np.sin(theta), np.zeros(len(theta))]).transpose()

# Direction of the Sun pointing from the Earth (opposite of earthDir)
def sunV(theta):
    return -earthDir(theta)

'''
The following helper functions were used in TEST_Perfect_Conditions
'''

# Tilt vector at the winter solstice. Points in positive x direction with y=0.
def tiltV(phi = tilt0):     
    return np.array([np.sin(phi), 0, np.cos(phi)])

# Rodrigues rotation formula. Default rotation around the tilt    
def rodV(v, theta, k = tiltV()):    
    # v = np.array([[1,2,3],[4,5,6], [7,8,9], [10, 11, 12], [13, 14, 15]])
    # k = np.array([1,2,3])
    # theta = np.array([0,1,2,3,4]).reshape(-1,1)
    
    theeta = theta.reshape(-1,1) # Makes theta into a single column vector (transposes). Is necessary
    
    v1 = v*np.cos(theeta) # First term.
    v2 = np.cross(k,v)*np.sin(theeta) # Second term 
    v3 = k*np.dot(v,k).reshape(-1,1)*(1-np.cos(theeta)) # Third term

    return v1+v2+v3 # Return their sum as is on the Wikipedia page.

# The plane of Earth's equator
def planeV(theta, phi=tilt0):
    
    # theta = how much rotate.
    # Initially the vector points towards the sun on the winter solstice.
    # Rotates around the tilt vector i.e the Earth's axis.
    
    planeInit = np.array([[-np.cos(phi)]*len(theta), [0]*len(theta), [np.sin(phi)]*len(theta)]).transpose()
    
    return rodV(planeInit, theta, k = tiltV(phi))

# The plane of Earth's equator
def planeV2(theta, phi=tilt0):
    
    # theta = how much rotate.
    # Initially the vector points towards the sun on the winter solstice.
    # Rotates around the tilt vector i.e the Earth's axis.
    
    planeInit = np.array([[-np.cos(phi)]*len(theta), [0]*len(theta), [np.sin(phi)]*len(theta)]).transpose()
    
    return planeInit