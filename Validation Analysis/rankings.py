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
    'Kidney_Cortex': 73,
    
    'Muscle_Skeletal_237': 237, 
    'Whole_Blood_237': 237,
    'Skin_Sun_Exposed_Lower_leg_237': 237, 
    'Thyroid_237': 237,
    'Lung_237': 237,
    
    'Muscle_Skeletal_73': 73,
    'Whole_Blood_73': 73,
    'Skin_Sun_Exposed_Lower_leg_73': 73,
    'Thyroid_73': 73,
    'Lung_73': 73
}
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
    tissue_name = tissue if not tissue.split('_')[-1].isdigit() else "_".join(tissue.split(sep='_')[:-1])
    ip_folder = '../Centrality Computation/' + tissue
    
    gene_list = pd.read_csv('../Original Dataset/Preprocessed Files/' + tissue_name + '/genes.csv', header=0, index_col=0)
    gene_order = pd.read_excel('Gene Ordering.xlsx', sheet_name=tissue_name, header=None, index_col=None).loc[:,0]
    
    rankings = fun(ip_folder, gene_list, gene_order)
    op_file = 'Rankings/ranks_' + centrality + '.xlsx'
    with pd.ExcelWriter(
            op_file,
            engine="openpyxl", 
            mode="a" if os.path.exists(op_file) else "w"
            ) as writer:
        rankings.to_excel(writer, sheet_name=tissue, header=True, index=True)
    