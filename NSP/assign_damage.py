# -*- coding: utf-8 -*-
"""
Created on Thu May 29 08:32:34 2014

@author: chiaracasotto
"""
import numpy as np

def assign_damage(limits,disp,H,noStorey):
    # Limits state definition
    # Assign damage state to each analysis
    disp.insert(0, np.zeros_like(disp[0]))
    H.insert(0, float(0))
    I = []
    for ls in range(0,len(limits)):
        for i in range(0,noStorey):
            a = np.divide(np.array(disp[i+1])-np.array(disp[i]),H[i+1]) #convert displacement to inter-storey-drift
            b = np.nonzero(a>limits[ls]) # find where drifts exceed limit states
            if len(b[0]) == 0: 
                find = len(a)-1
            else:
                find = b[0][0]
            I.append(find)

    LS_index = zip(*[iter(I)]*noStorey)
    LS_global = [min(ele) for ele in LS_index]
    disp_profile = np.empty([noStorey,len(limits)])
    for i in range(0,noStorey):
        disp_profile[i,:] = [disp[i+1][ele] for ele in LS_global]
    disp_profile = disp_profile.tolist()
#    
    return [disp_profile]