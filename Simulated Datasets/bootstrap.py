# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 01:49:08 2025

@author: sugyani
"""

#from envVar import setThreads
#setThreads(1)

# %% Co-Expression Network Construction
def CoExpressionNetwork(data, alpha = 0.01, kind = 'spearman'):
    '''
    This function constructs the coexpression network for the input gene expression dataset and returns the list of edges in the network.

    Parameters
    ----------
    data : pandas DataFrame
        The gene expression matrix. Rows are samples and Columns are genes.
    alpha : float, optional
        The alpha value cutoff for fdr correction. The default is 0.01.
    kind : 'pearson' or 'spearman', optional
        The type of correlation coefficient to be computed. The default is 'spearman'.

    Returns
    -------
    numpy ndarray of dimensions m x 2.
        Each row is an edge of the co-expression network.
    '''
    '''
    from corals.correlation.full.matmul import full_matmul_symmetrical as correlation
    from corals.correlation.utils import derive_pvalues
    from statsmodels.stats.multitest import multipletests
    import numpy as np
    
    s, n = data.shape
    
    r = correlation(data, correlation_type=kind)
    p = derive_pvalues(r, s)
    '''
    
    from scipy.stats import spearmanr
    from statsmodels.stats.multitest import multipletests as fdr
    import numpy as np
    
    s, n = data.shape
    p = spearmanr(data)[1]    
    indices = np.triu_indices(n, k= 1)
    p_flat = p[indices]
    rejected, _, _, _ = fdr(p_flat, alpha=0.01, method='fdr_bh')
    
    adj_matrix = np.zeros((n,n))
    adj_matrix[indices] = rejected
    return np.argwhere(adj_matrix)
    
# %% Constructs one Bootstrapped sample
def BootstrapSample(data):
    '''
    This function constructs a bootstrapped sample dataset, constructs the corresponding co-expression network and returns the edge list and the terminal list for the same.

    Parameters
    ----------
    data : pandas DataFrame
        The gene expression matrix. Rows are samples and Columns are genes.

    Returns
    -------
    edges : numpy ndarray of dimensions m x 2.
        Each row is an edge of the co-expression network.
    '''
    
    import random
    
    s, n = data.shape
    draw = random.choices(data.index, k=s)
    sample = data.loc[draw,:]
    edges = CoExpressionNetwork(sample)
    return edges