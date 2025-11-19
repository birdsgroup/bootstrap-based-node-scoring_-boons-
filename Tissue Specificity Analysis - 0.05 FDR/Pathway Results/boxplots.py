# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 18:24:50 2025

@author: HP
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

colors = ['#000000', '#0072B2', '#E69F00', '#009E73']
parameter_names = ['$\\mathtt{obs}$', '$\\mu$', '$\\mu-\\sigma$', '$\\mu-2\\sigma$']
file_names = ['obs', 'mu', 'mu-sigma', 'mu-2sigma']

# %% The Function
def boxplots(pathway, Tissues, gtype, centrality):
    for i in range(4):
        print(file_names[i])
        plot_data_list = []
        for tissue in Tissues:
            print(tissue)
            folder = tissue
            if '_' in tissue and tissue.split(sep='_')[-1].isdigit():
                folder = "_".join(tissue.split(sep='_')[:-1])                    
            all_genes = pd.read_csv('../../Original Dataset/Preprocessed Files/' + folder + '/genes.csv', header=0, index_col=None, sep=',')
            specific_genes = pd.read_csv('../' + gtype + ' Genes/' + pathway + '.tsv', sep = '\t')
            specific_indices = all_genes[all_genes['gene_name'].isin(specific_genes['Gene'])].index
            other_indices = all_genes[~(all_genes['gene_name'].isin(specific_genes['Gene']))].index

            deg = pd.read_csv('../../Centrality Computation/' + tissue + '/original_' + centrality + '.csv', header=None).iloc[0,:]        
            df = pd.read_csv('../../Centrality Computation/' + tissue + '/sample_' + centrality + '.csv', header=None, index_col=0)
            df.columns = all_genes.index

            mu = df.mean(axis = 0)
            std = df.std(axis = 0)
            mu_2sigma = mu - (2 * std)
            mu_sigma = mu - std

            parameters = {
                0: deg,
                1: mu,
                2: mu_sigma,
                3: mu_2sigma
            }
                
            plot_data = pd.DataFrame(columns=['value', 'gene_type', 'Tissue'])
            plot_data['value'] = parameters[i]
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
        plt.title(parameter_names[i], color = '#843C0C', fontsize=18)
        plt.savefig('boxplots/' + centrality + '_' + pathway + '_' + file_names[i] + '.pdf')
        plt.close()


# %% Degree Centrality
gtype = 'Elevated'
centrality = 'degree'
boxplots('Pancreas', ['Thyroid', 'Pancreas', 'Muscle_Skeletal_73'], gtype, centrality)
boxplots('Pituitary', ['Muscle_Skeletal', 'Pituitary', 'Kidney_Cortex'], gtype, centrality)

# %% PageRank Centrality
gtype = 'Elevated'
centrality = 'pagerank'
boxplots('Pancreas', ['Thyroid', 'Pancreas', 'Muscle_Skeletal_73'], gtype, centrality)
boxplots('Pituitary', ['Muscle_Skeletal', 'Pituitary', 'Kidney_Cortex'], gtype, centrality)
