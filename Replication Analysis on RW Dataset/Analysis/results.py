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
tissue_name = 'Muscle_Skeletal'
centrality = 'pagerank'
klim = 1000
palette = list(sns.color_palette("colorblind", n_colors=10).as_hex())

# %% Replication Analysis
print('Replication Analysis')
op_folder = 'Replication Results/' + centrality
if not os.path.exists(op_folder):
    os.makedirs(op_folder)

dis_tissue = tissue_name + '_gtex'
rep_tissue = tissue_name + '_recount'

dis_ranking = pd.read_excel('Rankings/ranks_' + centrality + '.xlsx', sheet_name=dis_tissue, header=[0,1], index_col=0)
rep_ranking = pd.read_excel('Rankings/ranks_' + centrality + '.xlsx', sheet_name=rep_tissue, header=[0,1], index_col=0)

reference = dis_ranking['rankings'].to_dict(orient='series')
rankings = rep_ranking['rankings'].to_dict(orient='series')

colors = dict(zip(dis_ranking['rankings'].columns, palette))
filepath = op_folder + '/CAT_' + tissue_name + '.pdf'
analysis.Plot(rankings, reference, klim, s=706, n=len(dis_ranking), plottype='cat', analysistype='R', colors=colors, path=filepath)
filepath = op_folder + '/Recall_' + tissue_name + '.pdf'
analysis.Plot(rankings, reference, klim, s=706, n=len(dis_ranking), plottype='recall', analysistype='R', colors=colors, path=filepath)
    