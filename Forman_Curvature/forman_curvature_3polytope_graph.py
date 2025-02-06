import numpy as np
import networkx as nx

def forman(graph):
  # input:
  # graph (numpy array) - the Adjacency Matrix of the desired graph. Must be a planar graph to run this code, and 3-polyhedral graphs are also 3-vertex connected.
  # returns:
  # forman_dict (dictionary) - each key is an edge (indexed by its position in the poset constructed within this function) and the value is the edge's Forman curvature.
    forman_dict = {} # keys are edges, values are its forman ricci curvature
    
    # construct face lattice 
    G_nx = nx.Graph(graph)

    # Check if the graph is planar and get the planar embedding
    # networkx
    is_planar, embedding_nx = nx.check_planarity(G_nx)

    # Construct poset of 1-skeleton
    # add vertices
    vert_elms = [] # a list 1,...,n

    for i in range(1, len(graph[0]) + 1):
        vert_elms = vert_elms + [i]

    # add edges
    edge_elms = []
    edge_dict = {} # keys are edge indices, values are the indicestwo vertices it contains

    # and relations
    relations = []

    for vert in vert_elms:
        vert_mat_index = vert - 1

        neighbors = [] # poset indices of neighbors
        for j in range(len(graph[0])):
            if graph[vert_mat_index][j] == 1:
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

    # Construct new poset
    total_elms = vert_elms + edge_elms + face_elms

    comb_poly_poset = Poset((total_elms, relations))
    
    # Now compute Forman Ricci curvature from this poset!
    n_verts = len(vert_elms)
    n_edges = len(edge_elms)
    n_faces = len(face_elms)
    
    index_first_edge = edge_elms[0]
    index_last_edge = edge_elms[-1]
    
    index_first_face = face_elms[0]
    index_last_face = face_elms[-1]
    
    # pick an edge
    for edge in range(index_first_edge, index_last_edge + 1):  
        # pick out which faces the edge is contained in 
        faces_to_check = []
        for k in range(index_first_face, index_last_face + 1):
            if comb_poly_poset.compare_elements(edge,k) == -1:
                faces_to_check = faces_to_check + [k]
    
        # pick out which vertices e contains
        verts_to_check = []
        for h in range(1, n_verts + 1):
            if comb_poly_poset.compare_elements(h,edge) == -1:
                verts_to_check = verts_to_check + [h]
            if len(verts_to_check) == 2:
                break
        
        # pick out relevant other edges to check
        # edges that share a face with e
        share_a_face = []
        for f in faces_to_check:
            for j in range(index_first_edge, index_last_edge + 1):
                if comb_poly_poset.compare_elements(j,f) == -1:
                    share_a_face = share_a_face + [j]
        
        # edges that share a vertex with e
        share_a_vert = []
        for v in verts_to_check:
            for j in range(index_first_edge, index_last_edge + 1):
                if comb_poly_poset.compare_elements(v,j) == -1:
                    share_a_vert = share_a_vert + [j]
        
        # examine relationship between e and other edges
        e_parallel_neighbor_vec = []
        for o in share_a_face:
            if o not in share_a_vert:
                e_parallel_neighbor_vec = e_parallel_neighbor_vec + [o]
        for q in share_a_vert:
            if q not in share_a_face:
                e_parallel_neighbor_vec = e_parallel_neighbor_vec + [q]
        
        # count everything up and add it to the dict!
        forman_curv = len(faces_to_check) + len(verts_to_check) - len(e_parallel_neighbor_vec)
        forman_dict[edge] = forman_curv
        
    return(forman_dict)        
