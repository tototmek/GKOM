def loop_subdivision(vertices, faces):
    print("Performing Loop subdivision surface")
    for vertex in vertices:
        for i in range(3):
            vertex[i] = 0.67 * vertex[i]
        for i in range(6, 8):
            vertex[i] = 0.67 * vertex[i]
    print("Warning: not implemented yet!")
    return (vertices, faces)
