def forman(poly):
    # input:
    # poly (Sage polytope object)
    # output:
    # forman_dict (dictionary) each key is the index of an edge in the face lattice, value is its forman ricci curvature
    
    forman_dict = {}
    
    f_vec = poly.f_vector()
    
    n_verts = f_vec[1]
    n_edges = f_vec[2]
    n_faces = f_vec[3]
    
    c_poly = CombinatorialPolyhedron(poly)
    
    index_first_edge = n_verts + 1
    index_last_edge = index_first_edge + n_edges - 1
    
    index_first_face = index_last_edge + 1
    index_last_face = index_first_face + n_faces - 1
    
    # pick an edge
    for i in range(index_first_edge, index_last_edge + 1):
        e = c_poly.face_by_face_lattice_index(i)
        
        # pick out which faces e is contained in 
        faces_to_check = []
        for k in range(index_first_face, index_last_face + 1):
            face = c_poly.face_by_face_lattice_index(k)
            if e.is_subface(face):
                faces_to_check = faces_to_check + [k]
        
        # pick out which vertices e contains
        verts_to_check = []
        for h in range(1, n_verts + 1):
            vertex = c_poly.face_by_face_lattice_index(h)
            if vertex.is_subface(e):
                verts_to_check = verts_to_check + [h]
                
        # pick out relevant other edges to check
        # edges that share a face with e
        share_a_face = []
        for f in faces_to_check:
            face = c_poly.face_by_face_lattice_index(f)
            for j in range(index_first_edge, index_last_edge + 1):
                other_edge = c_poly.face_by_face_lattice_index(j)
                if other_edge.is_subface(face):
                    share_a_face = share_a_face + [j]
        
        # edges that share a vertex with e
        share_a_vert = []
        for v in verts_to_check:
            vertex = c_poly.face_by_face_lattice_index(v)
            for j in range(index_first_edge, index_last_edge + 1):
                other_edge = c_poly.face_by_face_lattice_index(j)
                if vertex.is_subface(other_edge):
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
        forman_dict[i] = forman_curv
        
    return(forman_dict)        
