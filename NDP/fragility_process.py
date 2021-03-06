# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 15:12:45 2014

@author: chiaracasotto
"""
import numpy as np
from common.mle import mle
from common.conversions import from_median_to_mean

def count_to_poe(dcm,totblg):
    dpm = np.matrix(np.empty([dcm.shape[0],dcm.shape[1]]))
    fr = np.matrix(np.empty([dcm.shape[0],dcm.shape[1]])) #change here dimensions
    for line in range(0,dcm.shape[0]):
        for ls in range(0,dcm.shape[1]):
            dpm[line,ls] = np.divide(dcm[line,ls],totblg) # probability of occurance of damage
            acc = -dpm[line,:ls]
            cc = acc.tolist()
            cdm = [1]+cc[0]
            fr[line,ls] = sum(cdm) # probability of exceedance of damage
            fr = fr.round(5)
            fr = fr.__abs__()
    return [fr]
    
def fragility_process(dcm,totblg,im,noLS):
    
    [fr] = count_to_poe(dcm,totblg)
    
    # Export fragility points to csv
    #cd = os.getcwd()
    #output_file = cd+'/outputs/cumulative_damage_matrix.csv'
    #header = ['IML', 'no.blgs', 'Damage States']
    #dat1 = np.zeros(len(fr))
    #dat3 = []
    #for j in range(0, len(fr)):
    #    dat1[j] = im.tolist()[j][0]
    #    dat3.append([fr[j,:].tolist()[n] for n in range(0,noLS+1)]) # I don't know how to print fr in separeted columns
    #col_data = [dat1, [totblg]*len(dat1), dat3]
    #n_lines = len(fr)
    #print_outputs(output_file,header,n_lines,col_data)
    
    #Sort the matrices according to Intensity Measure Levels
    dcm = np.matrix(np.empty(fr.shape))
    I = np.argsort(im, axis=0)
    FR = fr[I,:]
    IM = im[I,:]
    log_meanSa, log_stSa = [],[]
    
    # Fit number of buildings exceeding each level of damage with Maximum Likelihood regression method
    for j in range(1,FR.shape[2]):
        damage = FR[:,0,j]*totblg #number of buildings exceeding damage j
        dint = damage.astype(int)
        nc = dint.transpose()
        num_collapse = nc.tolist()
        IML = [IM[i,0,0] for i in range(0,len(IM))]
        [mu, sigma]=mle(num_collapse, IML, totblg)
        log_meanSa.append(mu)
        log_stSa.append(sigma)
        
        print "LS", j
        print "mu=",mu
        print "sigma=",sigma
        
    return [log_meanSa, log_stSa, FR, IML]
    
