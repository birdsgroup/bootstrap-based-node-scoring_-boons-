# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 22:09:30 2026

@author: HP
"""

import pandas as pd
import random
import os

# %% Global variables
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

op_file = "Gene Ordering.xlsx"

# %% Ordering of genes for each tissue
for tissue in Tissues:
    print(tissue)
    
    # Set the seed -- this seed is same as the seed generated while creating the population
    with open('../' + tissue + '/seed.txt', 'r') as seed_file:
        seed = int(seed_file.read())
    seed_file.close()
    random.seed(seed)
    
    orig_file = '../' + tissue + '/orig_' + str(n) + '.csv'
    orig = pd.read_csv(orig_file, header=0, index_col=0).T
    new_order = pd.Series(random.sample(list(orig.columns), k=n))
    
    orig.columns.to_series().to_csv('../' + tissue + '/genes.csv', header=False, index=False)    
    with pd.ExcelWriter(
            op_file, 
            engine="openpyxl", 
            mode="a" if os.path.exists(op_file) else "w"
            ) as writer:
        new_order.to_excel(writer, sheet_name=tissue, header=False, index=False)
        
    
