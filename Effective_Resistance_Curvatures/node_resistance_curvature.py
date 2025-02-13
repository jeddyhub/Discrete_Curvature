import numpy as np

def node_res_curvature(adj_mat):
  # input: adj_mat (numpy array) - the Adjacency Matrix of the graph
  # returns: node_curvature (numpy array) - Node resistance curvature at each vertex

  ones_vector = np.ones(adj_mat[0].size)
  Degree = np.diag(ones_vector @ adj_mat)
  L = Degree - adj_mat

  # construct Gamma
  GammaInverse = np.linalg.pinv(L)

  # construct effective resistance matrix Omega
  Omega = np.empty([adj_mat.shape[0], adj_mat.shape[1]])

  for i in range(adj_mat.shape[0]):
    for j in range(adj_mat.shape[1]):
        Omega[i,j] = GammaInverse[i,i] + GammaInverse[j,j] - 2 * GammaInverse[i,j]

  # compute node resistance curvature vector
  node_curvature = np.empty(adj_mat.shape[0])

  for i in range(adj_mat.shape[0]):
      node_curvature_i = 1
      for j in range(adj_mat.shape[0]):
          if adj_mat[i,j] != 0:
              node_curvature_i = node_curvature_i - (0.5 * Omega[i,j] * adj_mat[i,j])
      node_curvature[i] = node_curvature_i

  return node_curvature
