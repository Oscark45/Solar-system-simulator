# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:10:38 2020

@author: Oscar
"""

import numpy as np
from scipy.integrate import odeint # This is used only for comparison
import matplotlib.pyplot as plt

def RK4(x0, y0, x, h, ecc): 
    def dodt(t, theta): 
        return (1 + ecc*np.cos(theta))**2 / (1-ecc**2)**(3/2) 
    
    n = int(np.round((x-x0)/h))
    theta = y0
    t = x0
    THETA = np.zeros(n+1)
    
    for i in range(1, n + 1): 
        k1 = h * dodt(t, theta) 
        k2 = h * dodt(t + h/2, theta + k1/2) 
        k3 = h * dodt(t + h/2, theta + k2/2) 
        k4 = h * dodt(t + h, theta + k3) 
  
        # Update the values of t and theta
        t = t + h 
        theta = theta + 1/6*(k1 + 2*k2 + 2*k3 + k4) 
        THETA[i] = theta
  
    return THETA

# Elliptical orbit differential equation
def planetFunction(theta, time,  e):
    return (1 + e * np.cos(theta))**2 / (1 - e**2)**(3/2)

# Elliptical orbit differential equation solved with odeint 
# (ONLY USED FOR COMPARISON)
def ellipticalOrbit(e, timeVector, theta0 = 0):
    
     # If length is zero, add a zero to the beginning
    if len(timeVector) == 1:   
        timeVector = np.insert(timeVector, 0, 0)
        
    angle = odeint(planetFunction, theta0, timeVector, args = (e,)) 
    
    return angle 

N = 525600
yearMinute = np.linspace(0,2*np.pi, N+1) 

def plot_errors():
    fig = plt.figure()
    for e in np.array([0.0167, 0.0934, 0.2056, 0.4]):
        rk4 = RK4(0, 0, 2*np.pi, 2*np.pi/N, e)
        ode = ellipticalOrbit(e, yearMinute).reshape(N+1,)
        error = (rk4[1:]-ode[1:])/ode[1:] # Ignore 0
        error = np.insert(error, 0, 0)
        plt.plot(yearMinute, error, label = '$\epsilon=${}'.format(e))

    plt.legend()
    plt.xlabel(r'$\theta$', fontsize = 16)
    plt.ylabel(r'($\theta_{RK4} - \theta_{odeint})/\theta_{odeint}$', fontsize = 16)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    plt.tick_params(axis='both', labelsize=14)
    plt.title('RK4 vs scipy.integrate.odeint', fontsize = 16)

# Uncomment this if you want to plot the comparison between RK4 and odeint
#plot_errors()
