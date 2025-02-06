import numpy as np

def res_curvature(adj_mat):
  # input: adj_mat (numpy array) - the Adjacency Matrix of the graph
  # returns: resistance_curvature (numpy array) - Effective resistance curvature at each vertex
  # NOTE: this is the effective resistance curvature notion developed by KAREL DEVRIENDT, ANDREA OTTOLINI, AND STEFAN STEINERBERGER
  # in the paper GRAPH CURVATURE VIA RESISTANCE DISTANCE - Discrete Applied Mathematics, 2024
  
  # construct Laplacian
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

  # compute effective resistance curvature vector
  ones_vector = np.ones(adj_mat.shape[0])
  resistance_curvature = np.linalg.solve(Omega, ones_vector)

  return resistance_curvature
