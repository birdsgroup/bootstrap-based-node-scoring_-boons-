#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 21:13:36 2024

@author: sugyani
"""

#from envVar import setThreads
#setThreads(1)

# %% Packages
import pandas as pd
import numpy as np
from numpy import round
import random
from os import makedirs

import bootstrap
import centrality

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

# %% Input
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
B = 1000

for tissue in Tissues.keys():
    for n in [1000]: #[1000, 500, 100]:
        print(tissue, n, sep='\t')
        outfolder = tissue + '/' + str(n)
        makedirs(outfolder)
        
        # Set the seed -- this seed is same as the seed generated while creating the population
        with open(tissue + '/seed.txt', 'r') as seed_file:
            seed = int(seed_file.read())
        seed_file.close()
        random.seed(seed)
        np.random.seed(seed)
        
        # Population
        print('Population')
        pop_file = tissue + '/pop_' + str(n) + '.csv'
        population = pd.read_csv(pop_file, header=0, index_col=None, dtype=float)
        fun(population, 'pop', n, outfolder)
                
        # Observed Dataset
        print('Observed Dataset')
        observed = population.sample(n=Tissues[tissue], axis='index', replace=False)
        observed.to_csv(outfolder + '/observed.csv', header=True, index=True)
        fun(observed, 'obs', n, outfolder, B=B)
                
        # Replication Datasets
        for p in [100, 80, 60]:
            print('Replication Dataset', p, sep='\t')
            s = int((p/100)*Tissues[tissue])
            replication = population.sample(n=s, axis='index', replace=False)
            replication.to_csv(outfolder + '/replication_' + str(p) + '.csv', header=True, index=True)
            fun(replication, 'rep_' + str(p), n, outfolder, B=B)
        
        if tissue == 'Muscle_Skeletal':
            for s in [237, 73, 53]:
                print('Replication Dataset', s, sep='\t')
                replication = population.sample(n=s, axis='index', replace=False)
                replication.to_csv(outfolder + '/replication_' + str(s) + '.csv', header=True, index=True)
                fun(replication, 'rep_' + str(s), n, outfolder, B=B)
        
        '''
        # %%% Original Data
        # Original Observed
        print('Original Observed')
        orig_file = tissue + '/orig_' + str(n) + '.csv'
        original = pd.read_csv(obs_file, header=0, index_col=0).T
        fun(original, 'orig', n, outfolder, B=B)        
        '''
        del population
        