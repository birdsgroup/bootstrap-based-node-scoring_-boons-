# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 22:04:15 2026

@author: HP
"""

import pandas as pd
import os

import analysis

# %% Global Variables
Tissues = {
    'Muscle_Skeletal_gtex': 706,
    'Muscle_Skeletal_recount': 53
    }
tissue_name = 'Muscle_Skeletal'
centrality = 'pagerank'
if not os.path.exists('Rankings'):
    os.makedirs('Rankings')

# %% The function
def fun(ip_folder: 'str', gene_list, gene_order):
    measure = pd.read_csv(ip_folder + '/' + centrality + '.csv', header=None, index_col=None, sep=',').loc[0,:]
    measure.index = gene_list.index
    measure = measure[gene_order]
    
    sample_measure = pd.read_csv(ip_folder + '/sample_' + centrality + '.csv', header=None, index_col=0, sep=',')
    sample_measure.columns = gene_list.index
    sample_measure = sample_measure.loc[:, gene_order]
    
    results = analysis.computeranks(measure, sample_measure)    
    return results

# %% 
for tissue in Tissues:
    print(tissue)    
    ip_folder = '../Centrality Computation/' + tissue
    
    gene_list = pd.read_csv('../Original Dataset/Preprocessed Files/' + tissue + '/genes.csv', header=0, index_col=0)
    gene_order = pd.read_excel('Gene Ordering.xlsx', sheet_name=tissue_name, header=None, index_col=None).loc[:,0]
    
    rankings = fun(ip_folder, gene_list, gene_order)
    op_file = 'Rankings/ranks_' + centrality + '.xlsx'
    with pd.ExcelWriter(
            op_file,
            engine="openpyxl", 
            mode="a" if os.path.exists(op_file) else "w"
            ) as writer:
        rankings.to_excel(writer, sheet_name=tissue, header=True, index=True)
    