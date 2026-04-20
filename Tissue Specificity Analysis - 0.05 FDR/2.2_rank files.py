# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 06:32:56 2026

@author: HP
"""

import os
import pandas as pd

# %%
Tissues = ['Kidney_Cortex', 'Lung', 'Muscle_Skeletal', 'Pancreas', 'Pituitary', 'Stomach', 'Thyroid', 'Whole_Blood', 'Muscle_Skeletal_73', 'Muscle_Skeletal_237', 'Whole_Blood_73', 'Whole_Blood_237', 'Lung_237', 'Lung_73', 'Thyroid_237', 'Thyroid_73', 'Vagina']
Scorings = ['EstNS_0', 'BooNS_0', 'BooNS_1', 'BooNS_2', 'BPCIlo_25']

for centrality in ['degree', 'pagerank']:
    print(centrality)
    ipfile = '../Validation Analysis/Rankings/ranks_' + centrality + '.xlsx'
    
    for tissue in Tissues:
        print(tissue)
        if not os.path.exists('ranks_' + centrality + '/' + tissue):
            os.makedirs('ranks_' + centrality + '/' + tissue)
        df = pd.read_excel(ipfile, sheet_name=tissue, header=[0,1], index_col=0)
        scores = df['scores']
        idx = df.index.str.split('.').str[0]
        for method in Scorings:
            x = scores[method]
            x.index = idx
            x.to_csv('ranks_' + centrality + '/' + tissue + '/' + method + '.rnk', sep='\t', header=False, index=True)