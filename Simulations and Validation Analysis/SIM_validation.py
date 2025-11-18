# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 14:45:55 2024

@author: HP
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests as fdr
import random

from time import time

import plots

# %% Inputs and Global Variables
n = 400
B = 1000
klim = 200

SampleSizes = [73, 237, 670, 1000, 1500]

# %% Co-expression Network Construction
def compute_deg(data):
    p = spearmanr(data)[1]
    indices = np.triu_indices(n, k=1)
    p_flat = p[indices]
    rejected, _, _, _ = fdr(p_flat, alpha=0.01, method='fdr_bh')
    
    adj_matrix = np.zeros((n,n))
    adj_matrix[indices] = rejected
    adj_matrix = adj_matrix + adj_matrix.T
    return np.sum(adj_matrix[n//2:, :n//2], axis = 1)

def Bootstrapping(data_sample, s):
    # data_sample.shape() = s x n
    print("Bootstrapping")
    deg_b = np.zeros(shape = (B,n//2), dtype = int)
    for b in range(B):
        if b % 100 == 0:
            print(b)
        bootstrap_sample = data_sample.loc[random.choices(data_sample.index, k = s),:]
        deg_b[b,:] = compute_deg(bootstrap_sample)
    deg_bootstrap = np.mean(deg_b, axis = 0)
    std_bootstrap = np.std(deg_b, axis = 0)
    return deg_bootstrap, std_bootstrap

# %% Seed
import os
seed_file = 'Simulated Data/seed.txt'
if not os.path.exists(seed_file):
    seed = int(time())
    with open(seed_file, 'w') as file:
        print(seed, file = file)
    file.close()
else:
    with open(seed_file, 'r') as file:
        seed = int(file.read())
random.seed(seed)
np.random.seed(seed)

# Random Ordering
order = random.sample(range(n//2, n), n//2)

# %% Population Dataset Generation
print('Population Dataset Generation')
pop_size = 1000000
data_pop = pd.DataFrame(index=range(pop_size), columns=range(n))
for i in range(n//2):
    data_pop[i] = np.random.normal(size = pop_size)

for i in range(n//2, n):
    deg = random.randint(1, n//2)
    chosen_vars = random.sample(range(n//2), k=deg)
    alpha = np.zeros(shape=(n//2 + 1,))
    alpha[chosen_vars] = 0.995
    alpha[-1] = 0.1
    beta = 0.01
    
    data_pop[i] = pd.Series([1]*pop_size)
    noise = np.random.normal(size = pop_size)
    #data_pop[i] = data_pop.loc[:,range(n//2)] @ alpha[:-1] + (data_pop.loc[:,i] * alpha[-1]) + (beta * noise)
    
    data_pop.loc[:,i] = (data_pop.loc[:,i] * alpha[-1]) + (beta * noise)
    for j in range(n//2):
        data_pop.loc[:,i] += (data_pop.loc[:,j] * alpha[j])
    
dataset = data_pop.copy() ## dataset.shape() = s x n
deg_pop_orig = compute_deg(dataset)
del data_pop

deg_pop_orig = pd.Series(deg_pop_orig, index=range(n//2,n))
parameters_pop = {
    0: deg_pop_orig[order],
    1: None,
    2: None,
    3: None
}

# %% Observed and Bootstrap Dataset -- ObsDI
for s in SampleSizes:
    print(s)
    # Data Sample
    print('Observed Data Sampling')
    data_sample = dataset.loc[random.sample(list(dataset.index), k=s), :]
    deg_obs_1 = compute_deg(data_sample)

    # Bootstrapping
    deg_bootstrap_1, std_bootstrap_1 = Bootstrapping(data_sample, s)

    print('Parameters')
    deg_obs_1 = pd.Series(deg_obs_1, index=range(n//2,n))
    deg_bootstrap_1 = pd.Series(deg_bootstrap_1, index=range(n//2,n))
    std_bootstrap_1 = pd.Series(std_bootstrap_1, index=range(n//2,n))
    parameters = {
        0: deg_obs_1[order],
        1: deg_bootstrap_1[order],
        2: (deg_bootstrap_1 - std_bootstrap_1)[order],
        3: (deg_bootstrap_1 - (2 * std_bootstrap_1))[order]
    }
    
    # %%% Plots -- ObsD1
    # mu v/s sigma
    filepath = 'Simulated Data/validation/plot_' + str(s) + '.pdf'
    plots.muVsSigma(deg_bootstrap_1[order], std_bootstrap_1[order], s, filepath)

    # CAT Plot
    filepath = 'Simulated Data/validation/cat_' + str(s) + '.pdf'
    plots.Plot(parameters, parameters_pop, klim, s, n = len(order), plottype='cat', analysistype='V', path=filepath)

    # Recall @ k Plot
    filepath = 'Simulated Data/validation/recall_' + str(s) + '.pdf'
    plots.Plot(parameters, parameters_pop, klim, s, n = len(order), plottype='recall', analysistype='V', path=filepath)
