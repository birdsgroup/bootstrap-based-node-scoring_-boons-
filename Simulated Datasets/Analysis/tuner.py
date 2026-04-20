# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 15:22:32 2026

@author: HP
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% Global Variables
c_vals = np.arange(0, 5, 0.05)
#percentile_vals = [1, 2.5, 5, 7.5, 10, 25]
percentile_vals = np.arange(1, 50.5, 0.5)

n = 1000
SampleSizes = [706, 670, 237, 73]
centrality = 'pr'

# %% Functions
def computeCI(name, pop_rank, obs_measure, mu, sigma, quantiles, c):
    measures = {
        'EstNS': obs_measure - (c * sigma),
        'BPCIlo': quantiles,
        'rBPCIlo': (2 * obs_measure) - quantiles,
        'BooNS': mu - (c * sigma)
    }
    ranks = measures[name].rank(method='first')
    return ranks.corr(pop_rank, method = 'kendall')

# %% 
CIs = {
       'EstNS': pd.DataFrame(columns=SampleSizes, index=pd.Index(c_vals, name='c'), dtype=float),
       'BPCIlo': pd.DataFrame(columns=SampleSizes, index=pd.Index(percentile_vals, name='alpha'), dtype=float),
       'rBPCIlo': pd.DataFrame(columns=SampleSizes, index=pd.Index(percentile_vals, name='alpha'), dtype=float),
       'BooNS':  pd.DataFrame(columns=SampleSizes, index=pd.Index(c_vals, name='c'), dtype=float)
}

gene_order = pd.read_excel('Gene Ordering.xlsx', sheet_name='order', header=None, index_col=None).loc[:,0]
pop_measure = pd.read_csv('../Population/pop_' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
pop_measure = pop_measure[gene_order]
pop_rank = pop_measure.rank(method = 'first')

for size in SampleSizes:    
    obs_measure = pd.read_csv('../' + str(size) + '/obs_' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
    obs_measure = obs_measure[gene_order]

    sample_measure = pd.read_csv('../' + str(size) + '/obs_sample_' + centrality + '.csv', header=None, index_col=0, sep=',')
    sample_measure.columns = range(n)
    sample_measure = sample_measure.loc[:, gene_order]
    
    mu = sample_measure.mean(axis=0)
    sigma = sample_measure.std(axis=0)
    
    # EstNS and BooNS
    taus_1 = pd.Series()
    taus_2 = pd.Series()
    for c in c_vals:
        taus_1[c] = computeCI('EstNS', pop_rank, obs_measure, mu, sigma, quantiles=pd.Series(), c=c)
        taus_2[c] = computeCI('BooNS', pop_rank, obs_measure, mu, sigma, quantiles=pd.Series(), c=c)
    CIs['EstNS'].loc[:,size] = taus_1
    CIs['BooNS'].loc[:,size] = taus_2
    
    # BPCIlo and rBPCIlo
    taus_1, taus_2 = pd.Series(), pd.Series()
    for q in percentile_vals:
        quantiles = sample_measure.quantile(q=q/100, axis=0)
        taus_1[q] = computeCI('BPCIlo', pop_rank, obs_measure, mu, sigma, quantiles, c=0)
        
        quantiles = sample_measure.quantile(q= 1 - (q/100), axis=0)
        taus_2[q] = computeCI('rBPCIlo', pop_rank, obs_measure, mu, sigma, quantiles, c=0)
    CIs['BPCIlo'].loc[:,size] = taus_1
    CIs['rBPCIlo'].loc[:,size] = taus_2

# %% Write to Files
with pd.ExcelWriter("Tuning c and alpha_" + centrality + ".xlsx", engine="openpyxl") as writer:
    for sheet_name, ci in CIs.items():
        ci.loc['median'] = ci.median(axis='index')
        ci.loc['IQR'] = ci.quantile(q=0.75, axis='index') - ci.quantile(q=0.25, axis='index')
        ci.to_excel(writer, sheet_name=sheet_name, index=True, header=True)

# %% Box Plots
'''
for ci in CIs.keys():
    plt.figure()
    ax = CIs[ci].loc[:,SampleSizes].boxplot()
    ax.set_xticklabels(SampleSizes, rotation=90)
    plt.xlabel('Sample Size of Observed Dataset')
    plt.ylabel('Kendall\'s $\\tau$')
    plt.title(ci)
    
x = pd.Series()
for size in SampleSizes:
    x[size] = CIs['BooNS'][size].quantile(0.75) - CIs['BooNS'][size].quantile(0.25)
x.name = 'IQR for BooNS'
'''