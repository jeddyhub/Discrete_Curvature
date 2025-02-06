def i_sided_2faces(poly):
  # input:
  # poly (SageMath Polytope object)
  # output:
  # p_vector (list) - (p_3,p_4,p_5,...) wherein p_k describes the number of k-gonal 2-faces of the polytope
    num_i_sides = {} # keys are 3 (triangle), 4 (quadrilateral), 5 (pentagon), etc., values are how many of each kind of face.
    
    f_vec = poly.f_vector()
    
    n_verts = f_vec[1]
    n_edges = f_vec[2]
    n_faces = f_vec[3]
    
    c_poly = CombinatorialPolyhedron(poly)
    
    index_first_edge = n_verts + 1
    index_last_edge = index_first_edge + n_edges - 1
    
    index_first_face = index_last_edge + 1
    index_last_face = index_first_face + n_faces - 1
    
    # pick a face
    for i in range(index_first_face, index_last_face + 1):
        f = c_poly.face_by_face_lattice_index(i)
        num_sides = 0

        # how many edges does f contain?
        for e in range(index_first_edge, index_last_edge + 1):
            edge = c_poly.face_by_face_lattice_index(e)
            if edge.is_subface(f):
                num_sides += 1
        
        if num_sides in num_i_sides:
            num_i_sides[num_sides] += 1
        else:
            num_i_sides[num_sides] = 1
        
    # get a vector of keys so we can sort it
    key_list = []
    for key in  num_i_sides:
        key_list += [key]
    key_list = sorted(key_list)
    max_k = key_list[-1]
    
    p_vector = []
    for i in range(3, max_k +1):
        if i in num_i_sides:
            p_vector += [num_i_sides[i]]
        else:
            p_vector += [0]
        
    return(p_vector)
