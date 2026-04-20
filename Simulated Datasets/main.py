# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 07:13:50 2026

@author: HP
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from numpy import round
import random
import os
from time import time

import bootstrap
import centrality

# %% Global Variables
n = 1000
B = 1000
pop_size = 500000
SampleSizes = [706, 670, 237, 73]

pop_folder = 'Population'
if not os.path.exists(pop_folder):
    os.makedirs(pop_folder)

# %% The Function
def fun(dataset, dataset_type, n, outfolder, B=None):
    edges = bootstrap.CoExpressionNetwork(dataset)
    
    deg = centrality.DegreeCentrality(edges, n)
    pr = centrality.PageRankCentrality(edges, n)
    
    with open(outfolder + '/' + dataset_type + '_degree.csv', 'w') as file:
        print(*deg, sep=',', end='\n', file=file)
    file.close()
    with open(outfolder + '/' + dataset_type + '_pr.csv', 'w') as file:
        print(*round(pr,3), sep=',', end='\n', file=file)
    file.close()
    
    if B:
        print('Bootstrapping')
        for b in range(B):
            if b % 100 == 0:
                print(b)
                
            edges_boot = bootstrap.BootstrapSample(dataset)
            deg_boot = centrality.DegreeCentrality(edges_boot, n)
            pr_boot = centrality.PageRankCentrality(edges_boot, n)
            
            with open(outfolder + '/' + dataset_type + '_sample_degree.csv', 'a') as file:
                print(b, *deg_boot, sep=',', end='\n', file=file)
            file.close()
            with open(outfolder + '/' + dataset_type + '_sample_pr.csv', 'a') as file:
                print(b, *round(pr_boot,3), sep=',', end='\n', file=file)
            file.close()
    return

# %% Seed
seed_file = pop_folder + '/seed.txt'
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

# %% Population Dataset Generation
print('Population Dataset Generation')
population = pd.DataFrame(index=range(pop_size), columns=range(n))
for i in range(n//2):
    population[i] = np.random.normal(size = pop_size)

for i in range(n//2, n):
    deg = random.randint(1, n//2)
    Ni = random.sample(range(n//2), k=deg)
    
    alpha = np.zeros(shape=(n//2,))
    alpha[Ni] = 0.995
    
    beta_gene = 0.1
    beta_noise = 0.01
    
    population[i] = pd.Series([1]*pop_size)
    noise = np.random.normal(size = pop_size)
    #population[i] = population.loc[:,range(n//2)] @ alpha + (population.loc[:,i] * beta_gene) + (beta_noise * noise)
    
    population.loc[:,i] = (beta_gene * population.loc[:,i]) + (beta_noise * noise)
    for j in range(n//2):
        population.loc[:,i] += (population.loc[:,j] * alpha[j])
population.to_csv(pop_folder + '/pop_' + str(n) + '.csv', header=True, index=True)
fun(population, 'pop', n, pop_folder)

# %% Observed and Replication Datasets
for s in SampleSizes:
    print(s)
    
    if not os.path.exists(str(s)):
        os.makedirs(str(s))
    outfolder = str(s)
    
    # Observed Dataset
    print('Observed Dataset')
    observed = population.sample(n=s, axis='index', replace=False)
    observed.to_csv(outfolder + '/observed.csv', header=True, index=True)
    fun(observed, 'obs', n, outfolder, B=B)
    
    # Replication Datasets
    for p in [100, 80, 60]:
        print('Replication Dataset', p, sep='\t')
        s_prime = int((p/100)*s)
        replication = population.sample(n=s_prime, axis='index', replace=False)
        replication.to_csv(outfolder + '/replication_' + str(p) + '.csv', header=True, index=True)
        fun(replication, 'rep_' + str(p), n, outfolder, B=B)
    
    if s == 706:
        for s_prime in [237, 73, 53]:
            print('Replication Dataset', s_prime, sep='\t')
            replication = population.sample(n=s_prime, axis='index', replace=False)
            replication.to_csv(outfolder + '/replication_' + str(s_prime) + '.csv', header=True, index=True)
            fun(replication, 'rep_' + str(s_prime), n, outfolder, B=B)
    