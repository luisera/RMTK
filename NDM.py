# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Nonlinear Dynamic Procedure

# <markdowncell>

# The user should change only section 1 "Define Option"

# <codecell>

"""
Created on Mon Jun  9 15:53:53 2014

@author: chiaracasotto
"""

# Clear existing variables
def clearall():
    all = [var for var in globals() if var[0] != "_"]
    for var in all:
        del globals()[var]
clearall()

import numpy as np
from NDP.read_data import read_data
from NDP.fragility_process import fragility_process
from NDP.vulnerability_process import vulnerability_process
from common.export_vulnerability import export_vulnerability
from NDP.export_fragility import export_fragility

# <headingcell level=2>

# 1. Define Options

# <markdowncell>

# >####in_type (input_type)
# 0: input is 'dcm.csv', a Damage Count Matrix with number of buildings in each limit state <br />
# 1: input is 'edp.csv', a matrix with engineering demand corresponding to IM of each dynamic analysis <br />

# <codecell>

in_type = 0

# <markdowncell>

# >####vuln
# 0: derive fragility curves <br />
# 1: derive vulnerability curves from fragility curves <br />
# 
# >####iml
# array of intensity measure level used to discretise the fragility curves and get discrete vulnerability curves
# >####plotflag
# 2 integers for each plot: fragility curves, vulenarbility curve
# 1: plot <br />
# 0: don't plot <br />
# 
# >####IMlabel
# list of 1 strings defining the Intensity Measure on the x axis of the plots as ['m/s$^{2}$']
# Line width for plots
# >####fontsize
# Fontsize used for labels, graphs etc.

# <codecell>

vuln = 0
plotflag = [1, 1]
iml = np.linspace(0.1, 400, 100)
IMlabel = ['m/s$^{2}$']
linew = 2
fontsize = 14

# <headingcell level=2>

# 2. Read data from csv input file and Process data

# <markdowncell>

# Obtain: damage count matrix, total number of buildings analysed, Intensity Measures of each record, number of Limit States
# plot_feature = [plotflag, linew, fontsize, IMlabel, iml]
# [dcm,totblg,im,noLS] = read_data(in_type)

# <codecell>

plot_feature = [plotflag, linew, fontsize, IMlabel, iml]
[dcm,totblg,im,noLS] = read_data(in_type)

# <headingcell level=2>

# 3.a Derive Fragility

# <markdowncell>

# ransfor Damage Count Matrix into matrix of probability of exceedance each damage

# <codecell>

[log_meanSa,log_stSa, FR, IML] = fragility_process(dcm,totblg,im,noLS)

# <headingcell level=3>

# 3.a.2 Plot and Export fragility

# <codecell>

if vuln == 0:
    export_fragility(vuln, plot_feature, log_meanSa, log_stSa, IML, FR)

# <headingcell level=2>

# 3.b Derive Vulnerability curves from damage-to-loss ratios

# <codecell>

LR50 = vulnerability_process(vuln,iml,log_meanSa,log_stSa)

# <headingcell level=3>

# 3.b.2 Derive and export Vulnerability

# <codecell>

if vuln == 1:
    export_vulnerability(vuln, plot_feature, LR50, 0)

# <codecell>


