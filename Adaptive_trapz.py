# -*- coding: utf-8 -*-
"""
Created on Wed May 27 16:19:41 2020

@author: Oscar
"""

import numpy as np

def trapz(f, a, b, N = 100, index = 0):
    
    h = (b-a)/N
    x = np.linspace(a, b, N+1, dtype = int) # N+1 points make N subintervals
    y = f(x, index)
    yRight = y[1:] 
    yLeft = y[:-1]

    return h/2*np.sum(yLeft + yRight)

def adaptive_integration(f, a, b, eps, index = 0):
    
    n_limit = 10**7 # Upper limit to avoid infinite calling
    n = 2 # Start from a small base case

    int_n  = trapz(f, a, b, n, index)
    int_2n = trapz(f, a, b, 2*n, index)
    delta = abs(int_2n - int_n)
    
    while delta > eps and n < n_limit:
        int_n  = trapz(f, a, b, n, index)
        int_2n = trapz(f, a, b, 2*n, index)
        delta = abs(int_2n - int_n)
        n *= 2

    # Return the integral value and n or -n depending if
    # tolerance was not reached with upper limit
    if delta <= eps:
        return int_2n, n  
    else:
        return int_2n,-n
