# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 01:08:16 2025

@author: HP
"""

import pandas as pd
import matplotlib.pyplot as plt

# %% Global Variables
colors = ['#000000', '#0072B2', '#E69F00', '#009E73']
shapes = ['o', '^', 's', '*']
parameter_names = ['$\\mathtt{obs}$', '$\\mu$', '$\\mu-\\sigma$', '$\\mu-2\\sigma$']

# %% mu v/s sigma plot
def muVsSigma(mu, sigma, s, path):
    plt.figure()
    plt.scatter(mu, sigma, color = '#CC79A7')
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel('$\\mu$', fontsize=16)
    plt.ylabel('$\\sigma$', fontsize=16)
    plt.title('$\\mu$ v/s $\\sigma$ \n s = ' + str(s), fontsize=18)
    plt.savefig(path)
    plt.close()
    return

# %% Plot
def Plot(parameters: 'dict', reference: 'dict', klim: 'int', s: 'int', n: 'int', plottype: 'str' = 'cat', analysistype: 'str' = 'V', path: 'str' = None):
    plt.figure()
    for i in range(len(parameters)):
        j = 0 if analysistype == 'V' else i
        values = pd.Series(index=range(5,klim))        
        
        if plottype == 'recall':
            reference_set = reference[j].nlargest(klim).index
            
        for k in range(5,klim):
            if plottype == 'cat':
                reference_set = reference[j].nlargest(k).index
            parameter_set = parameters[i].nlargest(k).index
            
            values[k] = len(set(reference_set) & set(parameter_set)) / len(reference_set)
        plt.plot(values, label=parameter_names[i], color=colors[i])
    plt.plot(pd.Series(values.index/n, index=values.index), linestyle='--', color='#CC79A7', label='random')
    plt.legend()
    plt.ylim(0, 1)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel('k', fontsize=16)
    plt.ylabel('POG' if plottype == 'cat' else 'Recall @ k', fontsize=16)
    plt.title(('CAT Plot' if plottype == 'cat' else 'Recall @ k') + ' \n s = ' + str(s), fontsize=18)
    plt.savefig(path)
    plt.close()
    return

# %% Scatter Plots of Degree
def DegComp(obs, reference, s=None, pop=False):
    plt.figure()
    plt.scatter(reference, obs)
    plt.ylabel('Population Degree' if pop else 'Observed Degrees')
    plt.xlabel('Ground Truth' if pop else 'Population Degree')
    plt.title('GT vs. Population' if pop else 'Population vs. ' + str(s))
    plt.savefig('Simulated Data/pop.pdf' if pop else 'Simulated Data/' + str(s) + '.pdf')
    plt.close()
    return
