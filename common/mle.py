# -*- coding: utf-8 -*-
"""
Created on Thu May  8 18:18:30 2014

@author: chiaracasotto
"""
import numpy as np
import scipy as sci
import scipy.stats as stat
import scipy.optimize as optim

def mle(num_collapse, iml, tot):
    "This function computes the optimal fit of a function"
    def func(x):
        p = [stat.lognorm.cdf(i, x[0], loc=0, scale=x[1]) for i in iml]
        return -sci.sum(stat.binom.logpmf(num_collapse,tot,p))
    x0 = np.array([1, 1])
    x = optim.fmin(func, x0)
    sigma = x[0]
    mu = np.log(x[1])
    return mu, sigma