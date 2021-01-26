# -*- coding: utf-8 -*-
"""
Created on Fri May 22 12:37:50 2020

@author: Oscar
"""

import numpy as np
import itertools
import os
from RK4 import RK4

# The folder "Eccentricities" was used with odeint

try:
    os.mkdir("Eccentricities2")
except OSError:
    print("Creation of the directory has failed")
else:
    print("Successfully created")

N = 525600
t0 = 0
theta0 = 0
thetaF = 2*np.pi
h = 2*np.pi/N
yearMinute = np.linspace(0,2*np.pi, N+1) # 525600 minutes in a perfect year

# Calculate Earth the angles for each time step for various eccentricities

eccentricities = np.arange(0, 0.95, 0.05) # Exclude 0.95
planetE = np.array([0.0167, 0.0934, 0.2056]) # Special eccentricities

for e in itertools.chain(planetE, eccentricities):
    save_path = os.getcwd() + "\\Eccentricities2" + "\\ecc{:.4f}.txt".format(e)
    np.savetxt(save_path, RK4(t0, theta0, thetaF, h, e),\
               delimiter = ' ', newline = '\n', fmt = '%4.13f')
    


