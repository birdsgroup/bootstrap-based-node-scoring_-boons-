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
}
centrality = 'pagerank'
klim = 1000
palette = list(sns.color_palette("colorblind", n_colors=10).as_hex())

# %% Validation Analysis
print('Validation Analysis')
op_folder = 'Validation Results/' + centrality
if not os.path.exists(op_folder):
    os.makedirs(op_folder)

for tissue in Tissues:
    print(tissue)
    
    pop_ranking = pd.read_excel('Rankings/ranks_' + centrality + '.xlsx', sheet_name=tissue, header=[0,1], index_col=0)['rankings'].iloc[:,0]
    reference = {pop_ranking.name: pop_ranking}
    
    for s in [237, 73]:
        print(s)
        tissue_name = tissue + '_' + str(s)
        rankings_df = pd.read_excel('Rankings/ranks_' + centrality + '.xlsx', sheet_name=tissue_name, index_col=0, header=[0,1])
        rankings = rankings_df['rankings'].to_dict(orient='series')
        
        colors = dict(zip(rankings_df['rankings'].columns, palette))
        filepath = op_folder + '/CAT_Skin_' + str(s) + '.pdf' if tissue == 'Skin_Sun_Exposed_Lower_leg' else op_folder + '/CAT_' + tissue_name + '.pdf'
        analysis.Plot(rankings, reference, klim, s=s, n=len(pop_ranking), plottype='cat', analysistype='V', colors=colors, path=filepath)
        filepath = op_folder + '/Recall_Skin_' + str(s) + '.pdf' if tissue == 'Skin_Sun_Exposed_Lower_leg' else op_folder + '/Recall_' + tissue_name + '.pdf'
        analysis.Plot(rankings, reference, klim, s=s, n=len(pop_ranking), plottype='recall', analysistype='V', colors=colors, path=filepath)
    