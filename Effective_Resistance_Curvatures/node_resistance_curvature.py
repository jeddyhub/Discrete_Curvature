import numpy as np

def node_res_curvature(A):
    # Input: A (list) Adjacency Matrix (can be weighted if you want)
    # Returns: node_curvature (list) Node resistance curvature at each vertex
    
    # Convert adjacency matrix to numpy array
    A_np = np.array(A)
    n = len(A_np)
    
    # Degree matrix (diagonal matrix where D[i, i] is the degree of node i)
    Degree = np.diag(np.sum(A_np, axis=1))
    
    # Laplacian matrix
    L = Degree - A_np
    
    # Compute the pseudo-inverse of the Laplacian matrix
    L_inv = np.linalg.pinv(L)
    
    # Compute the effective resistance matrix (Omega)
    L_inv_diag = np.diag(L_inv)  # Extract diagonal elements
    Omega = L_inv_diag[:, None] + L_inv_diag[None, :] - 2 * L_inv
    
    # Compute node resistance curvature
    node_curvature = 1 - 0.5 * np.sum(Omega * A_np, axis=1)
    
    return node_curvature.tolist()
