import numpy as np

def link_res_curvature(A):
  # input: A (list) Adjacency Matrix (can be weighted if you want)
  # returns: link_curvature (list) link curvature of each edge

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

  # compute link resistance curvature
  link_curvature = np.zeros([n, n])

  for i in range(n):
      for j in range(n):
          if A[i][j] != 0:
              link_curvature[i][j] = (2 * (node_curvature[i] + node_curvature[j])) / Omega[i][j]

  return link_curvature.tolist()
