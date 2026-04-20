# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 01:08:16 2025

@author: HP
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['text.usetex'] = True

# %% Global Variables


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


# %% The Plots
def Plot(rankings: 'dict', reference: 'dict', klim: 'int', s: 'int', n: 'int', plottype: 'str' = 'cat', analysistype: 'str' = 'V', colors: 'dict' = None, path: 'str' = None):
    '''
    This function plots the CAT and the Recall @ k plots and generates an excel sheet containing the same values.

    Parameters
    ----------
    rankings : 'dict'
        The observed rankings to validate. 
        Each ranking forms one item with the score name as the key and the actual scores as the values corresponding to the key.
        Each ranking/scoring is a pandas series with the corresponding gene ids as index.
    reference : 'dict'
        The reference rankings with which to validate.
        For validation analysis, this has only one item: the actual rankings with which validation is performed.
        For replication analysis, this dictionary is similar to the 'rankings' dictionary. (The keys for both must be the same.)
    klim : 'int'
        The maximum value of k until which the plots are generated.
    s : 'int'
        Number of samples in the dataset. Required for the title of the plot.
    n : 'int'
        Number of genes in the dataset. Required to draw the baseline 'random' scoring.
    plottype : 'str', optional
        The type of plot -- 'cat' or 'recall'. 
        The default is 'cat'.
    analysistype : 'str', optional
        The type of analysis being performed. Use 'V' for validation analysis and 'R' for replication analysis
        The default is 'V'.
    colors : 'dict', optional
        The list of colors to be used for plotting. 
        Each item of the dictionary is the color to be used for the corresponding ranking. 
        Ensure that there is a color for each ranking.
        The color '#CC79A7' is used for the 'random' ranking.
        If no color is provided then the default matplotlib colors are used. The default is 'None'.
    path : 'str', optional
        The full path (including the filename with extension) for output plot and sheet.
        The default is None, in which case the plot is just shown and the sheet is not saved.

    Returns
    -------
    If a destination filename is provided in the path, then the function creates two files:
        1. The plot at the path.
        2. "<plottype>.xlsx" in the same folder. The corresponding values POG and recall values are stored in a sheet with the same name as the filename provided in the path. If this ".xlsx" file is already there, then a new sheet is appended.

    '''
    import os
    
    scorename_map = {
        'EstNS': r"\texttt{\textsc{EstNS}}",
        'BooNS': r"\texttt{\textsc{BooNS}}",
        'BPCIlo': r"\texttt{\textsc{BPCIlo}}",
        'rBPCIlo': r"\texttt{\textsc{rBPCIlo}}"
        }
    labelnames = dict()
    for rank_name in rankings:
        labelnames[rank_name] = scorename_map[rank_name.split('_')[0]] + "\\textsubscript{" + rank_name.split('_')[1] + "}"    
    
    DF = pd.DataFrame(index=range(1,klim+1), columns= ['random'] + list(rankings.keys()))
    DF.loc[:,'random'] = DF.index / n
    
    plt.figure()
    for rank_name in rankings:
        ref_name = next(iter(reference)) if analysistype == 'V' else rank_name        
        values = pd.Series(index=range(1,klim+1))
        
        if plottype == 'recall':
            reference_set = reference[ref_name].nsmallest(klim).index
            
        for k in range(1,klim+1):
            if plottype == 'cat':
                reference_set = reference[ref_name].nsmallest(k).index
            gene_set = rankings[rank_name].nsmallest(k).index            
            values[k] = len(set(gene_set) & set(reference_set)) / len(reference_set)
        
        DF.loc[:,rank_name] = values
        if colors:
            plt.plot(values, label=labelnames[rank_name], color=colors[rank_name])
        else:
            plt.plot(values, label=labelnames[rank_name])
    
    if path:
        op_filename = '/'.join(path.split('/')[:-1]) + '/' + plottype + '.xlsx'
        with pd.ExcelWriter(
                op_filename, 
                engine="openpyxl", 
                mode="a" if os.path.exists(op_filename) else "w"
                ) as writer:
            DF.to_excel(writer, sheet_name=path.split('/')[-1].split('.')[0], header=True, index=True)
    
    plt.plot(pd.Series(values.index/n, index=values.index), linestyle='--', color='#000000', label='$\\mathtt{random}$')
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    #plt.ylim(0, 1)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel('k', fontsize=16)
    plt.ylabel('POG' if plottype == 'cat' else 'Recall @ k', fontsize=16)
    plt.title(('CAT Plot' if plottype == 'cat' else 'Recall @ k') + ' \n s = ' + str(s), fontsize=18)
    plt.tight_layout()
    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.show()
    return

# %% Compute the ranks

c_vals = {
    'EstNS': [0,1,2],
    'BooNS': [0,1,2]
    }
alpha_vals = {
    'BPCIlo': [25, 49],
    'rBPCIlo': [25, 49]
    }

def computeranks(
        obs_measure: pd.Series, 
        sample_measure: pd.DataFrame, 
        c_vals: dict = c_vals, 
        alpha_vals: dict = alpha_vals
    ):
    '''
    This function computes takes as input the "obs" measures and the measures for each bootstrapped sample (i.e., distribution) and computes the different rankings.

    Parameters
    ----------
    obs_measure : pd.Series
        The observed measures. Index of the series is the gene id.
    sample_measure : pd.DataFrame
        Measurements of each bootstrapped sample. 
        The columns are the genes (indexed using their id) and rows are the corresponding bootstrap samples.
    c_vals : dict, optional
        A dictionary containing the values of "c" for both the measure-based rankings (EstNS and BooNS).
        The key is the ranking name and the corresponding value is the list of values for c.
        The default is [0,1,2] for both the measures.
    alpha_vals : dict, optional
        A dictionary containing the values of "alpha" for both the percentile-based rankings (BPCIlo and rBPCIlo).
        The key is the ranking name and the corresponding value is the list of values for alpha.
        The default is [25, 49] for both the measures.

    Returns
    -------
    rankings : dict
        Different ranking of the genes. 
        Keys are the ranking names and the corresponding value is the ranking -- these values are each pd.Series.
        Each ranking is named as <ranking name>_<c/alpha>_<corresponding value of c or alpha>.
        For example: the ranking for EstNS with c = 0 is named as "EstNS_c_0"

    '''
    
    mu = sample_measure.mean(axis=0)
    sigma = sample_measure.std(axis=0)
    
    measures = dict()
    for c in c_vals['EstNS']:
        measures['EstNS_' + str(c)] = obs_measure - (c * sigma)
        
    for c in c_vals['BooNS']:
        measures['BooNS_' + str(c)] = mu - (c * sigma)
        
    for q in alpha_vals['BPCIlo']:
        measures['BPCIlo_' + str(q)] = sample_measure.quantile(q=q/100, axis=0)
    
    for q in alpha_vals['rBPCIlo']:
        measures['rBPCIlo_' + str(q)] = (2 * obs_measure) - sample_measure.quantile(q=(1-q/100), axis=0)
    
    rankings = dict()
    for rank_name in measures:
        rankings[rank_name] = measures[rank_name].rank(method='first', ascending=False)
    
    measures = pd.DataFrame(measures)
    rankings = pd.DataFrame(rankings)
    mu.name = 'mu'
    sigma.name = 'sigma'
    results = pd.concat([mu, sigma, measures, rankings], axis = 1, keys=['mean', 'standard deviation', 'scores', 'rankings'])    
    return results

