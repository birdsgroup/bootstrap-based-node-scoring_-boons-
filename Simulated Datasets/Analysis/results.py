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
n = 1000
SampleSizes = [706, 670, 237, 73]
centrality = 'pr'
klim = 1000
palette = list(sns.color_palette("colorblind", n_colors=10).as_hex())

# %% Validation Analysis
print('Validation Analysis')
op_folder = 'Validation Results/' + centrality
if not os.path.exists(op_folder):
    os.makedirs(op_folder)

pop_ranking = pd.read_excel('Rankings/ranks_population.xlsx', sheet_name=centrality, header=0, index_col=0).iloc[:,0]
reference = {pop_ranking.name: pop_ranking}

for size in SampleSizes:
    print(size)    
    
    rankings_df = pd.read_excel('Rankings/ranks_obs_' + centrality + '.xlsx', sheet_name=str(size), index_col=0, header=[0,1])
    rankings = rankings_df['rankings'].to_dict(orient='series')
    
    colors = dict(zip(rankings_df['rankings'].columns, palette))
    filepath = op_folder + '/CAT_' + str(size) + '.pdf'
    analysis.Plot(rankings, reference, klim, s=size, n=n, plottype='cat', analysistype='V', colors=colors, path=filepath)
    filepath = op_folder + '/Recall_' + str(size) + '.pdf'
    analysis.Plot(rankings, reference, klim, s=size, n=n, plottype='recall', analysistype='V', colors=colors, path=filepath)

# %% Replication Analysis
print('Replication Analysis')
for size in SampleSizes:
    print(size)
    total_list = [100, 80, 60, 237, 73, 53]
    suffix_list = total_list[:3] if not size == 706 else total_list
    for p in suffix_list:
        op_folder = 'Replication Results_' + str(p) + '/' + centrality
        if not os.path.exists(op_folder):
            os.makedirs(op_folder)
        
        reference_df = pd.read_excel('Rankings/ranks_obs_' + centrality + '.xlsx', sheet_name=str(size), index_col=0, header=[0,1])
        rankings_df = pd.read_excel('Rankings/ranks_rep_' + str(p) + '_' + centrality + '.xlsx', sheet_name=str(size), index_col=0, header=[0,1])
        
        reference = reference_df['rankings'].to_dict(orient='series')
        rankings = rankings_df['rankings'].to_dict(orient='series')
        
        colors = dict(zip(rankings_df['rankings'].columns, palette))
        filepath = op_folder + '/CAT_' + str(size) + '.pdf'
        analysis.Plot(rankings, reference, klim, s=size, n=n, plottype='cat', analysistype='R', colors=colors, path=filepath)
        filepath = op_folder + '/Recall_' + str(size) + '.pdf'
        analysis.Plot(rankings, reference, klim, s=size, n=n, plottype='recall', analysistype='R', colors=colors, path=filepath)
    