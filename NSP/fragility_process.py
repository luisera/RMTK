# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 16:58:30 2014

@author: chiaracasotto
"""

import numpy as np
from NSP.spo2ida_method import spo2ida
from NSP.simplified_method import simplified_bilinear
from NSP.DF_method import DFfragility
from NSP.spo2ida_based.spo2ida_allTfunction import spo2ida_allT
from NSP.spo2ida_based.get_spo2ida_parameters import get_spo2ida_parameters

pw = 1
filletstyle = 3

def fragility_process(vulnerability,an_type,T, Gamma, w, dcroof, SPO, bUthd, noBlg, g, MC, Sa_ratios, plot_feature, N, Tc, Td):
    plotflag, linew, fontsize = plot_feature[0:3]
    allSa, allbTSa, allLR50, allbLR = [],[],[],[]     
    for blg in range(0,noBlg):
        # Derive median Sa value (median of Sa) of capacity for each Limit State and corresponding overall dispersion std(log(Sa))
        if an_type==0: # Ruiz-Garcia Miranda's method
            [SaT50, bTSa] = simplified_bilinear(T[blg], Gamma[blg], dcroof[blg], SPO[blg], bUthd[blg], g)
        elif an_type==2: # Dolsek and Fajfar's method
            [mc,a,ac,r,mf] = get_spo2ida_parameters(SPO[blg], T[blg], Gamma[blg]) # Convert MDoF into SDoF
            [SaT50,bTSa] = DFfragility(T[blg], Gamma[blg], dcroof[blg], SPO[blg], bUthd[blg], mc, r, g, Tc, Td)
        else: # Vamvatsikos and Cornell's method
            [mc,a,ac,r,mf] = get_spo2ida_parameters(SPO[blg], T[blg], Gamma[blg]) # Convert MDoF into SDoF
            [idacm, idacr] = spo2ida_allT(mc,a,ac,r,mf,T[blg],pw,plotflag[1],filletstyle,N,linew,fontsize) # apply SPO2IDA procedure
            [SaT50,bTSa] = spo2ida(idacm, idacr, mf, T[blg], Gamma[blg], g, dcroof[blg], SPO[blg], bUthd[blg], MC)

        # Converting the Sa(T1) to Sa(Tav), the common IM
        SaTlogmean_av, bTSa_av = np.log(SaT50)*Sa_ratios[blg], np.array(bTSa)*Sa_ratios[blg]
        allSa.append(SaTlogmean_av)
        allbTSa.append(bTSa_av)

    # Combine the fragility of each building in a single lognormal curve with
    # mean = weighted_mean(means) and std = SRSS(weighted_std(means),weighted_mean(stds))
    log_meanSa, log_stSa = [],[]
    for i in range(0,len(dcroof[0])):
        SaLS = [ele[i] for ele in allSa]
        StdSaLS = [ele[i] for ele in allbTSa]
        log_meanSa.append(np.average(SaLS,weights = w)) # weighted log-mean mean(log(Sa))
        log_stSa.append(np.sqrt(np.sum(w*(np.power((SaLS-log_meanSa[i]),2)+np.power(StdSaLS,2))))) # weighted log-std (dispersion)
    
    return [log_meanSa, log_stSa]