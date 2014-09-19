# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 09:29:11 2014

@author: chiaracasotto
"""

import numpy as np
import os
pi = 3.141592653589793

def DFfragility(T, Gamma, drlim, SPO, buthd, mc, r, g, Tc, Td):
#------------------------------------------------------------------------------    
# INPUT
# Cy     : base shear coefficient at yield (presently covered by Gamma and dry)
#          Cy = Say/g = Vy/W, where Say=Sa @ yield, Vy = base shear @ yield
# drlim  : median roof displacement value that defines the fragility. It can result 
#          from any EDP but it should be expressed in terms of the (median)
#          corresponding roof disp (just like we always do in pushovers anyway)
# dry    : roof yield displacement
# buthd  : dispersion (std of log data) characterizing the lognormal
#          distribution of "limit-state roof drift capacity" around drlim
# T      : ESDOF period (sec)
# Gamma  : the participation factor for the roof displacement(>1). Note that for
#          a tall building (or higher-mode influenced one) it is best if you get
#          this value from Say versus droofy estimated from modal response
#          spectrum analysis to include multiple modes. If you use the Gamma of
#          the first one only you will not do well enough (it tends to be
#          lower). See work of Katsanos & Vamva (2014). 
# Tc,Td  : constant accel-constant velocity  and constant velocity-constant
#          displacement corner periods of a Newmark-Hall type spectrum. Default
#          values (roughly taken from Dolsek & Fafjar's (2005) third set of
#          ground motions), are [0.5,1.8].
# mc     : end-of-plastic-plateau capping ductility.
# r      : residual plateau strength divided by yield strength
#
# g      : the value of "g" in units compatible with T and drlim, dy.
#          The default is 9.81m/s2, assuming that dy and drlim are in meters.
# OUTPUT
# Sa50   : the median Sa for the fragility, in units of "g"
# bTSa   : the total dispersion, including capacity and demand dispersions.
#------------------------------------------------------------------------------ 
    dry = SPO[1]    
    mlim=np.array(drlim)/dry
    
    if mlim.any()>10: 
        print 'Error: mlim should be less than 10'
        os._exit(1)
    if r>1 and r<0.25:
        print 'Error: rp should be within [0.25,1]'
        os._exit(1)
    if mc<1 and mc>2.5:
        print 'Error: mc should be within [1,2.5]'
        os._exit(1)
        
    # Get the (mc50, Rmc) point
    Tdstar=Td*np.sqrt(2-r)
    R0=1
    m0=1
    # Eq. 2 and 3 in Dolsek and Fajfar (2004) 
    if T<=Tc:
        c=0.7*(T/Tc)
    elif T<=Tdstar:
        DT=(T-Tc)/(Tdstar-Tc)
        c=(0.7 + 0.3*DT)
    else:
        c=1
    Rmc = c*(mc-m0) + R0
    # from Ruiz-Garcia and Miranda (2007)
    bthd_mc=1.957*(1/5.876 + 1/(11.749*(T+0.1)))*(1-np.exp(-0.739*(Rmc-1)))
    # Get median and fractiles. For lognormal: Median = mean * exp(0.5*sigma^2)
    mc50=mc/np.exp(0.5*np.power(bthd_mc,2))
    mc16=mc50*np.exp(-bthd_mc)
    mc84=mc50*np.exp(bthd_mc)
    
    # Now set Rmf as twice Rmc and get (mf50,Rmf) point
    Rmf=2*Rmc
    R0=Rmc
    m0=mc
    if T<=Tc:
        c=0.7*np.sqrt(r)*(T/Tc)^(1/np.sqrt(r))
    elif T<=Tdstar:
        c=0.7*np.sqrt(r)*(1-DT)+DT
    else:
       c=1
    # This is the mean mu given R
    mf_mean=(Rmf-R0)/c + m0
    bthd_mf=1.957*(1/5.876 + 1/(11.749*(T + 0.1)))*(1-np.exp(-0.739*(Rmf - 1)))
    # For lognormal: Median = mean * exp(0.5*sigma^2)
    mf50=mf_mean/np.exp(0.5*np.power(bthd_mf,2))
    mf16=mf50*np.exp(-bthd_mf)
    mf84=mf50*np.exp(bthd_mf)
    
    R=[0,1,Rmc,Rmf]
    mu16=[0,1,mc16,mf16]
    mu50=[0,1,mc50,mf50]
    mu84=[0,1,mc84,mf84]
    # Now we have fractiles and can invert. Use linear extrapolation for mlim values larger than mf. 
    R16=np.interp(np.array(mlim),np.array(mu84),np.array(R))
    R50=np.interp(np.array(mlim),np.array(mu50),np.array(R))
    R84=np.interp(np.array(mlim),np.array(mu16),np.array(R))
    
    # Go to an R value at 85% of the R50 for a biased estimate of "b"
    Rlim=0.85*R50
    m50Rlim=np.interp(np.array(Rlim),np.array(R),np.array(mu50))
    b=np.log(m50Rlim)/np.log(Rlim)
    
    bRSa=0.5*(np.log(R84)-np.log(R16))
    bUSa=buthd/b
    
    CR50 = mlim/R50
    Sa50 = 4*np.power(pi,2)*np.array(drlim)/(g*Gamma*CR50*np.power(T,2))
    bTSa = np.sqrt(np.power(bUSa,2) + np.power(bRSa,2))
    return [Sa50, bTSa]