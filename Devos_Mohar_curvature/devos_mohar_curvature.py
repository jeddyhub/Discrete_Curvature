import numpy as np
import networkx as nx

# Devos-Mohar curvature
# (for planar graphs embedded in the sphere)
# assigned to a vertex v:
# 1 - deg(v)/2 + sum_{f containing v} 1/size(f)
# where size(f) is the number of edges of the 2-face f

def devos_mohar_curvature(A):
  # input:
  # A (numpy array) - the Adjacency Matrix of the desired graph. Must be a planar graph to run this code, and 3-polyhedral graphs are also 3-vertex connected.
  # returns:
  # curvature (list) - Devos-Mohar curvature at each vertex

  # construct face lattice 
  G_nx = nx.Graph(A)
  n = len(A[0])

  # Check if the graph is planar and get the planar embedding
  is_planar, embedding_nx = nx.check_planarity(G_nx)

  # Construct poset of 1-skeleton
  # add vertices
  vert_elms = [] # a list 1,...,n

  for i in range(1, n + 1):
      vert_elms = vert_elms + [i]

  # add edges
  edge_elms = []
  edge_dict = {} # keys are edge indices, values are the indices (two vertices it contains)

  # and relations
  relations = []

  for vert in vert_elms:
      vert_mat_index = vert - 1

      neighbors = [] # poset indices of neighbors
      for j in range(n):
          if A[vert_mat_index][j] == 1:
              neighbors = neighbors + [j + 1]

      for buddy in neighbors:
          if vert < buddy:
              if len(edge_elms) == 0:
                  edge_elms = edge_elms + [vert_elms[-1] + 1]
                  edge_dict[edge_elms[-1]] = [vert, buddy]
                  relations = relations + [[vert, edge_elms[-1]]] + [[buddy, edge_elms[-1]]]
              else:
                  edge_elms = edge_elms + [edge_elms[-1] + 1]
                  edge_dict[edge_elms[-1]] = [vert, buddy]
                  relations = relations + [[vert, edge_elms[-1]]] + [[buddy, edge_elms[-1]]]

  # add faces
  face_elms = []
  face_dict = {} # key is the index of a face (in the poset lattice), feature is the first nx vertex list we find

  for edge in edge_dict:
      # Take in an edge, traverse its face to see which vertices are contained.
      two_vert_indices = edge_dict[edge]
      two_verts = []
      for i in two_vert_indices:
          two_verts = two_verts + [i-1]

      # first half-edge
      f1_vert_list = list(embedding_nx.traverse_face(v=two_verts[0], w=two_verts[1]))

      # test if this face has been accounted for yet
      test_face1 = []
      for face in face_dict:
          already_found_face = face_dict[face]
          if sorted(f1_vert_list) == sorted(already_found_face):
              test_face1 = test_face1 + [1]
              # if this face has already been acknowledged, take its index and add a relation
              relations = relations + [ [edge, face] ]

      # if this face has not been accounted for yet, add it to the dict / poset element list
      if len(test_face1) == 0:
          if len(face_elms) == 0:
              face_elms = face_elms + [edge_elms[-1] + 1]
              face_dict[face_elms[-1]] = f1_vert_list
              relations = relations + [ [edge, face_elms[-1]] ]
          else:
              face_elms = face_elms + [face_elms[-1] + 1]
              face_dict[face_elms[-1]] = f1_vert_list
              relations = relations + [ [edge, face_elms[-1]] ]

      # second half-edge
      f2_vert_list = list(embedding_nx.traverse_face(v=two_verts[1], w=two_verts[0]))

      # test if this face has been accounted for yet
      test_face2 = []
      for face in face_dict:
          already_found_face = face_dict[face]
          if sorted(f2_vert_list) == sorted(already_found_face):
              test_face2 = test_face2 + [1]
              # if this face has already been acknowledged, take its index and add a relation
              relations = relations + [ [edge, face] ]

      # if this face has not been accounted for yet, add it to the dict / poset element list
      if len(test_face2) == 0:
          if len(face_elms) == 0:
              face_elms = face_elms + [edge_elms[-1] + 1]
              face_dict[face_elms[-1]] = f2_vert_list
              relations = relations + [ [edge, face_elms[-1]] ]
          else:
              face_elms = face_elms + [face_elms[-1] + 1]
              face_dict[face_elms[-1]] = f2_vert_list
              relations = relations + [ [edge, face_elms[-1]] ]

  # for each vertex, look to see which faces contain it, and compute curvature
  # 1 - deg(v)/2 + sum_{f containing v} 1/size(f)
  ones_vec = np.ones(n)
  curvature = []
  for v in vert_elms:
    deg = ones_vec @ A[v-1]
    curv = 1 - (deg/2)
    for face in face_dict:
        if v in face_dict[face]:
          curv += (1/len(face_dict[face]))
    curvature.append(curv)

  return curvature
