# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 02:19:51 2025

@author: sugyani
"""

#from envVar import setThreads
#setThreads()

import numpy as np

# %% Degree Centrality -- General (Static) Graphs
def DegreeCentrality(edges, n, average = False):
    '''
    This function computes the Degree Centrality of every node in a network.

    Parameters
    ----------
    edges : numpy ndarray of dimensions m x 2.
        Each row is an edge of the co-expression network.
    n : int
        Number of nodes in the network.
    average : bool, optional
        If True, computes the average degree of the nodes, else returns the degree of every node. The default is False.

    Returns
    -------
    1-D numpy array of size n
        Every element is the degree centrality of the node representing the corresponding index.
    '''
    
    data_tab = np.unique(edges, return_counts=True)
    deg = np.zeros(shape = (n,), dtype = np.int16)
    deg[data_tab[0]] = data_tab[1]
    if average:
        return deg / n
    return deg

# %% PageRank Centrality -- General (Static) Graphs
def PageRankCentrality(edges, n, alpha = 0.85, beta = 0.15):
    '''
    This function computes the PageRank Centrality of every node in a network.

    Parameters
    ----------
    edges : numpy ndarray of dimensions m x 2.
        Each row is an edge of the co-expression network.
    n : int
        Number of nodes in the network.
    alpha : float, optional
        The alpha value. The default is 0.85.
    beta : float, optional
        The beta value -- usually set to (1 - alpha). The default is 0.15.

    Returns
    -------
    x : 1-D numpy array of size n
        Every element is the PageRank centrality of the node representing the corresponding index.
    '''
    
    from scipy.linalg import lu_factor, lu_solve
    
    A = np.zeros((n,n))
    A[edges[:,0], edges[:,1]] = 1
    A[edges[:,1], edges[:,0]] = 1        
    D = np.sum(A, axis=1)
    
    D_tilde = D.copy()
    D_tilde[ D_tilde==0 ] = 1
    
    M = -alpha * A
    np.fill_diagonal(M, D_tilde)
    beta_vec = beta * np.ones(shape=(n,))
    
    #y = lu_solve(lu_factor(M), beta_vec) # Works only if M is non-singular.
    y = np.linalg.solve(M, beta_vec) # Otherwise
    
    x = D_tilde * y
    return x