# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 05:59:27 2026

@author: HP
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
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
klim = 1000
palette = list(sns.color_palette("colorblind", n_colors=10).as_hex())

# %% Validation Analysis
print('Validation Analysis')
op_folder = 'Validation Results/' + centrality
if not os.path.exists(op_folder):
    os.makedirs(op_folder)

for tissue in Tissues:
    print(tissue)
    
    pop_ranking = pd.read_excel('Rankings/ranks_pop_' + centrality + '.xlsx', sheet_name=tissue, header=0, index_col=0).iloc[:,0]
    reference = {pop_ranking.name: pop_ranking}
    
    rankings_df = pd.read_excel('Rankings/ranks_obs_' + centrality + '.xlsx', sheet_name=tissue, index_col=0, header=[0,1])
    rankings = rankings_df['rankings'].to_dict(orient='series')
    
    colors = dict(zip(rankings_df['rankings'].columns, palette))
    filepath = op_folder + '/CAT_' + tissue + '.pdf'
    analysis.Plot(rankings, reference, klim, s=Tissues[tissue], n=n, plottype='cat', analysistype='V', colors=colors, path=filepath)
    filepath = op_folder + '/Recall_' + tissue + '.pdf'
    analysis.Plot(rankings, reference, klim, s=Tissues[tissue], n=n, plottype='recall', analysistype='V', colors=colors, path=filepath)

# %% Replication Analysis
print('Replication Analysis')
for tissue in Tissues:
    print(tissue)
    total_list = [100, 80, 60, 237, 73, 53]
    suffix_list = total_list[:3] if not tissue == 'Muscle_Skeletal' else total_list
    for p in suffix_list:
        op_folder = 'Replication Results_' + str(p) + '/' + centrality
        if not os.path.exists(op_folder):
            os.makedirs(op_folder)
        
        reference_df = pd.read_excel('Rankings/ranks_obs_' + centrality + '.xlsx', sheet_name=tissue, index_col=0, header=[0,1])
        rankings_df = pd.read_excel('Rankings/ranks_rep_' + str(p) + '_' + centrality + '.xlsx', sheet_name=tissue, index_col=0, header=[0,1])
        
        reference = reference_df['rankings'].to_dict(orient='series')
        rankings = rankings_df['rankings'].to_dict(orient='series')
        
        colors = dict(zip(rankings_df['rankings'].columns, palette))
        filepath = op_folder + '/CAT_' + tissue + '.pdf'
        analysis.Plot(rankings, reference, klim, s=Tissues[tissue], n=n, plottype='cat', analysistype='R', colors=colors, path=filepath)
        filepath = op_folder + '/Recall_' + tissue + '.pdf'
        analysis.Plot(rankings, reference, klim, s=Tissues[tissue], n=n, plottype='recall', analysistype='R', colors=colors, path=filepath)
    