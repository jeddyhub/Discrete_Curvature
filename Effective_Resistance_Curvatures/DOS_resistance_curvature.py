import numpy as np

def res_curvature(A):
  # input: A (list) Adjacency Matrix (can be weighted if you want)
  # returns: resistance_curvature (list) Steinerberger effective resistance curvature at each vertex

  # construct laplacian
  n = len(A[0])
  A_np = np.array(A)

  ones_vector = np.ones(n)
  Degree = np.diag(ones_vector @ A_np)
  L = Degree - A_np

  # construct Gamma
  GammaInverse = np.linalg.pinv(L)

  # construct effective resistance matrix Omega
  Omega = np.empty([n, n])

  for i in range(n):
    for j in range(n):
        Omega[i][j] = GammaInverse[i][i] + GammaInverse[j][j] - 2 * GammaInverse[i][j]

  # compute effective resistance curvature vector
  resistance_curvature = np.linalg.solve(Omega, ones_vector)

  return resistance_curvature.tolist()
