# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 22:09:30 2026

@author: HP
"""

import pandas as pd
import random
import os
from time import time

# %% Global variables
tissue = 'Muscle_Skeletal'
op_file = "Gene Ordering.xlsx"

# %% Seed
seed_file = 'seed.txt'
if not os.path.exists(seed_file):
    seed = int(time())
    with open(seed_file, 'w') as file:
        print(seed, file = file)
    file.close()
else:
    with open(seed_file, 'r') as file:
        seed = int(file.read())
random.seed(seed)

# %% Ordering of genes for each tissue
genes = pd.read_csv('../Original Dataset/Preprocessed Files/' + tissue + '_gtex/genes.csv', header=0, index_col=0)
new_order = pd.Series(random.sample(list(genes.index), k=len(genes)))
with pd.ExcelWriter(
        op_file, 
        engine="openpyxl", 
        mode="a" if os.path.exists(op_file) else "w"
        ) as writer:
    new_order.to_excel(writer, sheet_name=tissue, header=False, index=False)
