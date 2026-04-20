# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 18:15:00 2024

@author: HP
"""

import pandas as pd

# %% The Function
def fun(gtype, Tissues):
    output = gtype + '.gmt'

    with open(output, 'w') as file:
        for tissue in Tissues:
            specific_genes = pd.read_csv(gtype + ' Genes/' + tissue + '.tsv', sep = '\t')
            print(tissue, tissue, *specific_genes['Ensembl'], sep='\t', file=file, end='\n')

# %% Main Function
Tissues = ['Kidney_Cortex', 'Lung', 'Muscle_Skeletal', 'Pancreas', 'Pituitary', 'Stomach', 'Thyroid', 'Whole_Blood', 'Vagina']

for gtype in ['Elevated']: #['Elevated', 'Enriched']:
    if gtype == 'Enriched':
        fun(gtype, Tissues[:-1])
    else:
        fun(gtype, Tissues)