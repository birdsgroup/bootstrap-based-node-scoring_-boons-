# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 22:04:15 2026

@author: HP
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

import analysis

# %% Global Variables
n = 1000
SampleSizes = [706, 670, 237, 73]
centrality = 'pr'
if not os.path.exists('Rankings'):
    os.makedirs('Rankings')

# %% The function
def fun(ip_folder: 'str', ip_fname, gene_order, bias=False, pop_measure=None):
    tissue = ip_folder.split('/')[1]    
    
    measure = pd.read_csv(ip_folder + '/' + ip_fname + '_' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
    measure = measure[gene_order]
    
    sample_measure = pd.read_csv(ip_folder + '/' + ip_fname + '_sample_' + centrality + '.csv', header=None, index_col=0, sep=',')
    sample_measure.columns = range(n)
    sample_measure = sample_measure.loc[:, gene_order]
    
    results = analysis.computeranks(measure, sample_measure)    
    
    if bias and pop_measure is not None:
        if not os.path.isdir('Bias/' + centrality):
            os.makedirs('Bias/' + centrality)
        
        estimator_bias = measure - pop_measure
        bootstrap_bias = sample_measure.mean(axis=0) - measure
        
        plt.figure()
        sns.histplot(estimator_bias, kde=True, label='Estimator Bias')
        sns.histplot(bootstrap_bias, kde=True, label='Bootstrap Bias')
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.xlabel('Bias')
        plt.ylabel('Frequency')
        plt.title('Distribution of Bias_' + tissue)
        plt.tight_layout()
        plt.savefig('Bias/' + centrality + '/' + tissue + '.pdf')
        plt.close()
    
    return results

# %% Main Part
# Population Ranks
gene_order = pd.read_excel('Gene Ordering.xlsx', sheet_name='order', header=None, index_col=None).loc[:,0]
pop_measure = pd.read_csv('../Population/pop_' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
pop_measure = pop_measure[gene_order]
pop_rank = pop_measure.rank(method = 'first', ascending=False)
pop_rank.name = 'Population Rank'

op_file = 'Rankings/ranks_population.xlsx'
with pd.ExcelWriter(
        op_file,
        engine="openpyxl", 
        mode="a" if os.path.exists(op_file) else "w"
        ) as writer:
    pop_rank.to_excel(writer, sheet_name=centrality, header=True, index=True)
 
for size in SampleSizes:
    print(size)
    ip_folder = '../' + str(size)    
    for dataset in ['observed', 'replication']:
        if dataset == 'observed':              
            rankings = fun(ip_folder, 'obs', gene_order, bias=True, pop_measure=pop_measure)
            op_file = 'Rankings/ranks_obs_' + centrality + '.xlsx'
            with pd.ExcelWriter(
                    op_file, 
                    engine="openpyxl", 
                    mode="a" if os.path.exists(op_file) else "w"
                    ) as writer:
                rankings.to_excel(writer, sheet_name=str(size), header=True, index=True)       
        else:
            total_list = [100, 80, 60, 237, 73, 53]
            suffix_list = total_list[:3] if not size == 706 else total_list
            for p in suffix_list:
                ip_fname = 'rep_' + str(p)
                rankings = fun(ip_folder, ip_fname, gene_order)
                op_file = 'Rankings/ranks_' + ip_fname + '_' + centrality + '.xlsx'
                with pd.ExcelWriter(
                        op_file, 
                        engine="openpyxl", 
                        mode="a" if os.path.exists(op_file) else "w"
                        ) as writer:
                    rankings.to_excel(writer, sheet_name=str(size), header=True, index=True)