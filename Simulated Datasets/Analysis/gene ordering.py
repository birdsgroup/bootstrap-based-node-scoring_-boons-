# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 22:09:30 2026

@author: HP
"""

import pandas as pd
import random
import os

# %% Global variables
n = 1000

op_file = "Gene Ordering.xlsx"

# %% Ordering of genes
# Set the seed -- this seed is same as the seed generated while creating the population
with open('../Population/seed.txt', 'r') as seed_file:
    seed = int(seed_file.read())
seed_file.close()
random.seed(seed)

new_order = pd.Series(random.sample(range(n), k=n))
with pd.ExcelWriter(
        op_file, 
        engine="openpyxl", 
        mode="a" if os.path.exists(op_file) else "w"
        ) as writer:
    new_order.to_excel(writer, sheet_name='order', header=False, index=False)