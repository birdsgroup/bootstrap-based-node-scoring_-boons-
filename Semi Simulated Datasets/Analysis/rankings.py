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
if not os.path.exists('Rankings'):
    os.makedirs('Rankings')

# %% The function
def fun(ip_folder: 'str', ip_fname, gene_list, gene_order, bias=False, pop_measure=None):    
    tissue = ip_folder.split('/')[1]    
    
    measure = pd.read_csv(ip_folder + '/' + ip_fname + '_' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
    measure.index = gene_list
    measure = measure[gene_order]
        
    sample_measure = pd.read_csv(ip_folder + '/' + ip_fname + '_sample_' + centrality + '.csv', header=None, index_col=0, sep=',')
    sample_measure.columns = gene_list
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

# %% 
for tissue in Tissues:
    print(tissue)
    ip_folder = '../' + tissue + '/' + str(n)
    
    gene_list = pd.read_csv('../' + tissue + '/genes.csv', header=None, index_col=None).loc[:,0]
    gene_order = pd.read_excel('Gene Ordering.xlsx', sheet_name=tissue, header=None, index_col=None).loc[:,0]
    
    pop_measure = pd.read_csv(ip_folder + '/pop_' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
    pop_measure.index = gene_list
    pop_measure = pop_measure[gene_order]
    pop_rank = pop_measure.rank(method = 'first', ascending=False)
    pop_rank.name = 'Population Rank'
    
    op_file = 'Rankings/ranks_pop_' + centrality + '.xlsx'
    with pd.ExcelWriter(
            op_file,
            engine="openpyxl", 
            mode="a" if os.path.exists(op_file) else "w"
            ) as writer:
        pop_rank.to_excel(writer, sheet_name=tissue, header=True, index=True)
    
    for dataset in ['observed', 'replication']:
        if dataset == 'observed':              
            rankings = fun(ip_folder, 'obs', gene_list, gene_order, bias=True, pop_measure=pop_measure)
            
            op_file = 'Rankings/ranks_obs_' + centrality + '.xlsx'
            with pd.ExcelWriter(
                    op_file, 
                    engine="openpyxl", 
                    mode="a" if os.path.exists(op_file) else "w"
                    ) as writer:
                rankings.to_excel(writer, sheet_name=tissue, header=True, index=True)            
        else:
            total_list = [100, 80, 60, 237, 73, 53]
            suffix_list = total_list[:3] if not tissue == 'Muscle_Skeletal' else total_list
            for p in suffix_list:
                ip_fname = 'rep_' + str(p)
                rankings = fun(ip_folder, ip_fname, gene_list, gene_order)
                op_file = 'Rankings/ranks_' + ip_fname + '_' + centrality + '.xlsx'
                with pd.ExcelWriter(
                        op_file, 
                        engine="openpyxl", 
                        mode="a" if os.path.exists(op_file) else "w"
                        ) as writer:
                    rankings.to_excel(writer, sheet_name=tissue, header=True, index=True)