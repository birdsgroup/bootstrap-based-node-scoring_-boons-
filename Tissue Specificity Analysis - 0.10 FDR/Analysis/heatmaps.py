# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:52:00 2025

@author: HP
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['text.usetex'] = True

ScoreSystems = {
    'EstNS_0': r"\texttt{\textsc{EstNS}}\textsubscript{0}",
    'BooNS_0': r"\texttt{\textsc{BooNS}}\textsubscript{0}",
    'BooNS_1': r"\texttt{\textsc{BooNS}}\textsubscript{1}",
    'BooNS_2': r"\texttt{\textsc{BooNS}}\textsubscript{2}",
    'BPCIlo_25': r"\texttt{\textsc{BPCIlo}}\textsubscript{25}"
    }


# %% Heatmaps
def plot_hmap(centrality, gtype, Tissues, Paths):
    for ssystem in ScoreSystems:
        print(ssystem)        
        heatmap_data = pd.DataFrame(columns= Paths, index = Tissues, dtype=float) # rows are tissues and columns are paths
        
        for tissue in Tissues:
            filepath = '../Specificity Analysis/' + gtype + '_' + centrality + '/' + tissue + '/Project_' + ssystem + '/enrichment_results_' + ssystem + '.txt'
            if not os.path.exists(filepath):
                continue
            results = pd.read_csv(filepath, sep='\t')
            
            for index in results.index:
                path = results.loc[index, 'geneSet']
                heatmap_data.loc[tissue, path] = results.loc[index, 'enrichmentScore']
        
        heatmap_data.fillna(0, inplace=True)
        
        plt.figure()
        ax = sns.heatmap(heatmap_data, cmap='coolwarm', vmin=-1, vmax=1, xticklabels=True, yticklabels=True)
        ax.hlines([4, 10], *ax.get_xlim(), colors='white', linewidths=2)
        ax.vlines([4, 7], *ax.get_ylim(), colors='white', linewidths=2)
        plt.xticks(rotation=45, ha='right')
        #plt.yticks(fontsize=15)
        plt.xlabel('Gene Set ID\'s', fontsize=16)
        plt.ylabel('Tissues', fontsize=16)
        plt.title(ScoreSystems[ssystem], color = '#843C0C', fontsize=18)
        plt.tight_layout()
        plt.savefig('Heatmaps/' + centrality + '_' + ssystem + '.pdf')
        plt.close()
    
# %% Main Function
Tissues = ['Whole_Blood', 'Muscle_Skeletal', 'Lung', 'Thyroid', 'Pancreas', 'Pituitary', 'Stomach', 'Muscle_Skeletal_237', 'Lung_237', 'Thyroid_237', 'Kidney_Cortex', 'Vagina', 'Muscle_Skeletal_73',  'Lung_73', 'Thyroid_73']
Paths = ['Whole_Blood', 'Muscle_Skeletal', 'Lung', 'Thyroid', 'Pancreas', 'Pituitary', 'Stomach', 'Kidney_Cortex', 'Vagina']

for gtype in ['Elevated']:
    os.makedirs('Heatmaps')
    for centrality in ['degree', 'pagerank']:
        print(gtype, centrality)
        plot_hmap(centrality, gtype, Tissues, Paths)