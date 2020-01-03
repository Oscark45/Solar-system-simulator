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
import localSun5 as current
from datetime import datetime

# (1) Testing four times
fourTest = np.arange('2018-06-21T11:20:00', '2018-06-21T12:10:00', dtype = 'datetime64[10m]') 
fourTest2 = np.arange('2018-06-21T12:00:00', '2019-06-21T12:00:00', dtype = 'datetime64[31D]')

sunTest = current.localSun(30, 0, fourTest) # clat = 30, lon = 0, 4 datetime objects, tilt = 23.44

# Just showing that giving many vectors as parameters works
print('(1) Printing the observers vectors. Radial, polar, azimuthal.')
print('The are grouped as 5 x 3 radial, 5 x 3 polar and 5 x 3 azimuthal')
print(sunTest.obsV())
print('\nThis way you can print the first element, that is all the radial vectors:')
print("sunTest.obsV()[0] Which gives:\n")
print(sunTest.obsV()[0])
print('\nSimilarly with sunTest.obsV()[1] and sunTest.obsV()[2] you can get the polar and azimuthal vectors.\n')

print('(2) Testing the initial orientation at the 2019 winter solstice (04:19 UTC):\n')
print('Printing the picture:')

# (2) Plotting the situtation at the 2019 winter solstice

sunSolstice = current.localSun(90, 0, np.array([datetime.now()], dtype = 'datetime64[s]'))
sunSolstice = current.localSun(30, 0, np.array([np.datetime64('2019-12-22T04:19:00', 's')]))

fig = plt.figure()
from mpl_toolkits.mplot3d import Axes3D # This is apparently needed for the '3d' next line
ax = fig.gca(projection='3d')
ax.set_xlim3d(-1.5, 1.5)
ax.set_ylim3d(-1.5, 1.5)
ax.set_zlim3d(-1.5, 1.5)

colors = list(['r', 'g', 'b', 'k', 'y', 'm'])
# Red - observers radial vector
# Green - observers polar vector
# Blue - observers azimuthal vector
# Black - Tilt vector
# Yellow - Direction of Earth from the Sun
# Magenta - plane of Earth's equator (no brown availabe apparently)

import itertools
j = 0 

# Earth's position vector. Used for coordinates and direction
posEarth = current.earthDir(np.array([0]))*1.2

# Iterate through the observers vectors and put them where the Earth is
for v in itertools.chain(sunSolstice.obsV()): # with itertools we could go others besides sunNow.obsV() as well
    ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2] , v[0][0], v[0][1], v[0][2], length = 0.5 \
              , normalize = False, color = '{:}'.format(colors[j]))
    j += 1

# Add the tilt vector and plane vector to the same position
for v in itertools.chain(np.array([[current.tiltV()]])):
    ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2], v[0][0], v[0][1], v[0][2], length = 0.8 \
              , normalize = False, color ='{:}'.format(colors[j]))
    j += 1

# Plot the coordinate axes
for v in np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) :
    ax.quiver(0, 0, 0, v[0], v[1], v[2], length = 0.5, normalize = False, color = 'k')
    
for orientation in np.linspace(0, 2*np.pi, num=100):
    earthVector = current.planeV(np.array([orientation]))
    ax.quiver(posEarth[0][0], posEarth[0][1], posEarth[0][2], earthVector[0][0], earthVector[0][1], \
              earthVector[0][2], length = 0.25 , normalize = False, color = 'k')    

# Plot the position vector of Earth
w = current.earthDir(np.array([0]))
ax.quiver(0, 0, 0, w[0][0], w[0][1], w[0][2], length = 0.8, normalize = False, color = 'm')

print('Seems to be working fine!\n')

# (3) Test various methods
print('(3) Testing the various methods to see they work with matrices and vectors as should.')
print('The current implementation considerably improves the performance by using vectorization.\n')

print("a) Testing the rotation vector on the xy-plane around the z axis. Start with (1,0,0).")
print("Go through angles (0, 45, 90, ... , 315, 360)")
theta = np.linspace(0, 2*np.pi, num = 9)
print("Result:\n")
print(current.rodV(np.array([1,0,0]), theta, np.array([0, 0, 1])))
print("\nWorks fine! You can give a single vector and rotate it with many orientations.")

# (4) test the orientations for a few different times.
print("b) Now testing for the 3 vector system of the observer so rotate all the observers vectors")
print("Let's say we have vectors ([1,0,0], [0,1,0] [-1,0,0] [0,-1,0] [1,0,0]). In python this is an array:\n")
v1 = np.array([[1,0,0], [0,1,0], [-1,0,0], [0,-1,0], [1,0,0]])
print(v1)
print("\nThen another set ([1,0,0] [0,0,1] [-1,0,0] [0,0,-1] [1,0,0]). Again this is:")
v2 = np.array([[1,0,0], [0,0,1], [-1,0,0], [0,0,-1], [1,0,0]])
print(v2)
print("\nFinally let's just say we have a bunch of [1,0,0] vectors. Combinining all these 3 gives:")
v3 = np.array([[1,0,0], [1,0,0], [1,0,0], [1,0,0], [1,0,0]])
v4 = np.array([v1, v2, v3])
print(v4)
print("\nThis whole thing is basically an array with 3 elements and each element contains five 3 dimensional vectors.")
print("The first element would be the radial vectors corresponding to 5 (different) times and same with polar and azimuthal\n")
print("Let's now test with the rotation angles 45, 90, 135, 180 and 225 degrees. Needs to be 5 at this point. Rotational axis is again the z-axis")
print("For this we call rodV() for the vector v4[0] and orientation vector (45, 90, 135, 180, 225)")
theta2 = np.linspace(np.pi/4, 5/4 * np.pi, num = 5)
unitZ = np.array([0, 0, 1])
ultRotation = current.rodV(v4[0], theta2, unitZ)
print(ultRotation)
print("\nWorks fine for a single matrix now say just for the radial vectors. Fails for the massive thing with three 5x3 matrices. But that's probably fine for now")

# 5 Testing the azimuth method which uses a rejection vector
print("\nc) Testing vectors for the azimuth method:")
print("So far we can have just a vector w1 and and w2 which is w1 rotated by 90 degrees. So they are:\n")
w1 = np.array([[1,0,0], [0,1,0], [-1,0,0], [0,-1,0], [1,0,0]])
w2 = current.rodV(w1, np.array([np.pi/2]), np.array([0,0,1]))
print(w1)
print("\n")
print(w2)
print("\nFor this we first test the  rejection vector. The important term is the following: self.sunV - np.dot(r, self.sunV)*r")
print("\nIf for example r = w1 and the dot product thing is (5,4,3,2,1) then the matrix implemenation gives:\n")
wRej = np.array([5,4,3,2,1])
print(wRej.reshape(-1,1) * w1)
print("Works. Good! This would give the following azimuths for the test:\n")
print(np.degrees(sunTest.azimuth()))
print("\nLet's test that the projection vector is on the plane, thus it should be orthogonal to the radial vectors")
print("\nThe radial vectors for this test are:")
a = sunTest.radialV()
print(sunTest.radialV())
print("\nThe azSun() method gives the following vectors:")
b = sunTest.azSun()
print(sunTest.azSun())
print("\nThe individual dot products are:")
print(current.dotVectors(sunTest.radialV(), sunTest.azSun()))
print("Practically 0. Good! Rejection seems to work")




