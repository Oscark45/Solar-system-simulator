# -*- coding: utf-8 -*-
# file_name.py
# Python 3.6

"""
Author:     Oscar Kaatranen
Created:    % 12/08/2019 $
Modified:   %(date)$ 

Description

"""

import numpy as np
from scipy.integrate import odeint
from vpython import *

from localSun import ellipticalOrbitArb


scene = canvas(width = 1000, ehight = 10, range = 300)
scene.forward = vector(0.5, -0.2, -1) # to change point of view

sun = sphere(pos = vector(0, 0, 0), radius=50, color = color.yellow)
planet1 = sphere(pos = vector(400, 0, 0), radius=30, color = color.blue, make_trail = True)
planet2 = sphere(pos = vector(400, 0, 0), radius=30, color = color.red, make_trail = True)
planet3 = sphere(pos = vector(400, 0, 0), radius=30, color = color.orange, make_trail = True)
planet4 = sphere(pos = vector(400, 0, 0), radius=30, color = color.green, make_trail = True)

# Polar unit vector
def polarV(theta):
        
    return np.array([np.cos(theta), np.sin(theta), np.zeros(len(theta))]).transpose()

thetas = np.linspace(0,2*np.pi, 1001)

circularPos = polarV(thetas)


# Elliptical orbit differential equation
def planetFunction(theta, time,  e):
    
    return (1 + e * np.cos(theta))**2 / (1 - e**2)**(3/2)

# Polar equation of an ellipse
def polarEllipse(theta, e):
    
    return (1-e**2)/(1+e*np.cos(theta))

e1 = 0.2056
e2 = 0.9
e3 = 0.45
Time = np.linspace(0, 2*np.pi, 1001)
theta0 = 0

angle1 = odeint(planetFunction, theta0, Time, args = (e1,))
angle1 = angle1.reshape(1001,)

angle2 = odeint(planetFunction, theta0, Time, args = (e2,))
angle2 = angle2.reshape(1001,)

angle3 = odeint(planetFunction, theta0, Time, args = (e3,))
angle3 = angle3.reshape(1001,)


x_values1 = np.cos(angle1)*polarEllipse(angle1, e1)
y_values1 = np.sin(angle1)*polarEllipse(angle1, e1)

x_values2 = np.cos(angle2)*polarEllipse(angle2, e2)
y_values2 = np.sin(angle2)*polarEllipse(angle2, e2)

x_values3 = np.cos(angle3)*polarEllipse(angle3, e3)
y_values3 = np.sin(angle3)*polarEllipse(angle3, e3)

for t in arange(0, 1000, 1):
    rate(300)
    
    planet1.pos = vector(400*circularPos[t][0], 400*circularPos[t][1], circularPos[t][2])
    planet2.pos = vector(400*x_values1[t], 400*y_values1[t], 0)
    planet3.pos = vector(400*x_values2[t], 400*y_values2[t], 0)
    planet4.pos = vector(400*x_values3[t], 400*y_values3[t], 0)

# Comparing the angles corresponding to different times such as 3/2 * pi

# Angles (or more accurately times) corresponding to indices 1, 10, 23, 250, 750
angles = np.array([2*np.pi/1000, 2*np.pi/100, 23*2*np.pi/1000, np.pi/2, 3/2*np.pi])
anglesE3 = np.take(angle3, [1, 10, 23, 250, 750])

results = np.zeros(5)

i = 0
for ang in angles:
    
    results[i] = ellipticalOrbitArb(e3, np.array([ang]))[1][1]
    
    i += 1
    
print("The difference vector is:")
print(results - anglesE3)




