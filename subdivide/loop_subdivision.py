def loop_subdivision(vertex_array, face_array):
    print("Performing Loop subdivision surface")
    # TODO
    vertices = vertex_array.copy()
    faces = face_array.copy()
    for vertex in vertices:
        for i in range(3):
            vertex[i] = 0.67 * vertex[i]
    print("Warning: not implemented yet!")
    return (vertices, faces)
