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

Tissues = {
    'Muscle_Skeletal': 706, 
    'Whole_Blood': 670,
    'Skin_Sun_Exposed_Lower_leg': 605, 
    'Thyroid': 574, 
    'Lung': 515, 
    
    'Stomach': 324,     
    'Pancreas': 305, 
    'Pituitary': 237, 
    'Brain_Cerebellum': 209, 
    'Brain_Cortex': 205, 
    
    'Vagina': 141, 
    'Brain_Amygdala': 129, 
    'Uterus': 129, 
    'Brain_Substantia_nigra': 114, 
    'Kidney_Cortex': 73    
}
n = 1000
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
       'EstNS': pd.DataFrame(columns=Tissues.keys(), index=pd.Index(c_vals, name='c'), dtype=float),
       'BPCIlo': pd.DataFrame(columns=Tissues.keys(), index=pd.Index(percentile_vals, name='alpha'), dtype=float),
       'rBPCIlo': pd.DataFrame(columns=Tissues.keys(), index=pd.Index(percentile_vals, name='alpha'), dtype=float),
       'BooNS':  pd.DataFrame(columns=Tissues.keys(), index=pd.Index(c_vals, name='c'), dtype=float)
}

for tissue in Tissues:
    print(tissue)
    
    gene_list = pd.read_csv('../' + tissue + '/genes.csv', header=None, index_col=None).loc[:,0]
    gene_order = pd.read_excel('Gene Ordering.xlsx', sheet_name=tissue, header=None, index_col=None).loc[:,0]
    
    pop_measure = pd.read_csv('../' + tissue + '/' + str(n) + '/pop_' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
    pop_measure.index = gene_list
    pop_measure = pop_measure[gene_order]
    pop_rank = pop_measure.rank(method = 'first')

    obs_measure = pd.read_csv('../' + tissue + '/' + str(n) + '/obs_' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
    obs_measure.index = gene_list
    obs_measure = obs_measure[gene_order]

    sample_measure = pd.read_csv('../' + tissue + '/' + str(n) + '/obs_sample_' + centrality + '.csv', header=None, index_col=0, sep=',')
    sample_measure.columns = gene_list
    sample_measure = sample_measure.loc[:, gene_order]
    
    mu = sample_measure.mean(axis=0)
    sigma = sample_measure.std(axis=0)
    
    # EstNS and BooNS
    taus_1 = pd.Series()
    taus_2 = pd.Series()
    for c in c_vals:
        taus_1[c] = computeCI('EstNS', pop_rank, obs_measure, mu, sigma, quantiles=pd.Series(), c=c)
        taus_2[c] = computeCI('BooNS', pop_rank, obs_measure, mu, sigma, quantiles=pd.Series(), c=c)
    CIs['EstNS'].loc[:,tissue] = taus_1
    CIs['BooNS'].loc[:,tissue] = taus_2
    
    # BPCIlo and rBPCIlo
    taus_1, taus_2 = pd.Series(), pd.Series()
    for q in percentile_vals:
        quantiles = sample_measure.quantile(q=q/100, axis=0)
        taus_1[q] = computeCI('BPCIlo', pop_rank, obs_measure, mu, sigma, quantiles, c=0)
        
        quantiles = sample_measure.quantile(q= 1 - (q/100), axis=0)
        taus_2[q] = computeCI('rBPCIlo', pop_rank, obs_measure, mu, sigma, quantiles, c=0)
    CIs['BPCIlo'].loc[:,tissue] = taus_1
    CIs['rBPCIlo'].loc[:,tissue] = taus_2

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
    ax = CIs[ci].loc[:,Tissues.keys()].boxplot()
    ax.set_xticklabels(Tissues.keys(), rotation=90)
    plt.xlabel('Tissues')
    plt.ylabel('Kendall\'s $\\tau$')
    plt.title(ci)
    
x = pd.Series()
for tissue in Tissues:
    x[tissue] = CIs['boons'][tissue].quantile(0.75) - CIs['boons'][tissue].quantile(0.25)
x.name = 'IQR for boons'
'''