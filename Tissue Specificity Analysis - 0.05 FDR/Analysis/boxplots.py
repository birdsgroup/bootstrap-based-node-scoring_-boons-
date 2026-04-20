# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 18:24:50 2025

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
os.makedirs('boxplots')

# %% The Function
def boxplots(pathway, Tissues, gtype, centrality):
    ipfile = '../../Validation Analysis/Rankings/ranks_' + centrality + '.xlsx'
    for ssystem in ScoreSystems:
        print(ssystem)
        plot_data_list = []
        for tissue in Tissues:
            print(tissue)
            folder = tissue
            if '_' in tissue and tissue.split(sep='_')[-1].isdigit():
                folder = "_".join(tissue.split(sep='_')[:-1])                    
            all_genes = pd.read_csv('../../Original Dataset/Preprocessed Files/' + folder + '/genes.csv', header=0, index_col=0, sep=',')
            idx = all_genes.index.str.split('.').str[0]
            specific_genes = pd.read_csv('../' + gtype + ' Genes/' + pathway + '.tsv', sep = '\t')            
            specific_indices = all_genes.loc[idx.isin(specific_genes['Ensembl']),:].index
            other_indices = all_genes.loc[~(idx.isin(specific_genes['Ensembl'])),:].index
            
            df = pd.read_excel(ipfile, sheet_name=tissue, header=[0,1], index_col=0)
            plot_data = pd.DataFrame(columns=['value', 'gene_type', 'Tissue'])            
            plot_data['value'] = df['scores'][ssystem]
            plot_data.loc[specific_indices, 'gene_type'] = 'Specific Genes'
            plot_data.loc[other_indices, 'gene_type'] = 'Other Genes'
            plot_data['Tissue'] = tissue
            plot_data_list.append(plot_data)
                    
        plot_data = pd.concat(plot_data_list, ignore_index=True)
        plt.figure()
        sns.boxplot(x = 'Tissue', y = 'value', hue = 'gene_type', data=plot_data, palette='colorblind')
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.ylabel('Centrality Scores', fontsize=16)
        plt.xlabel('Tissues', fontsize=16)
        plt.title(ScoreSystems[ssystem], color = '#843C0C', fontsize=18)
        plt.savefig('boxplots/' + centrality + '_' + pathway + '_' + ssystem + '.pdf')
        plt.close()

# %% BoxPlots
gtype = 'Elevated'
for centrality in ['degree', 'pagerank']:
    boxplots('Pancreas', ['Thyroid', 'Pancreas', 'Muscle_Skeletal_73'], gtype, centrality)
    boxplots('Pituitary', ['Muscle_Skeletal', 'Pituitary', 'Kidney_Cortex'], gtype, centrality)
