import numpy as np

def catmull_clark_subdivision(vertices, cells: np.array):
    print("Performing Catmull-Clark subdivision surface")
    print(cells)
    original_points = {}
    faces = {}
    edges = {}
    size = cells.shape[0]
    for ind_cell in range(cells.shape[0]):

        cell_position = tuple(cells[ind_cell])

        faces[cell_position] = {'face_point': None} # for points and face_points) fejsy się nie powtarzają więc chyba jest git
        face_points = []

        for index in cell_position:
            if index not in original_points.keys():
                v = vertices[index]

                point = {
                    'point': v,
                    'faces': [],
                    'edges': []
                }
                original_points[index] = point # może tu coś się zjebało
            else:
                point = original_points[index]

            # Now point has a reference to its face
            point['faces'].append(cell_position)
            face_points.append(point)

        faces[cell_position]['points'] = face_points

        ## getting the facepoint

        points = np.empty((np.size(cell_position), 8))
        for i, index in enumerate(cell_position):
            vertex = np.array(vertices[index])
            points[i] = vertex

        faces[cell_position]['face_point'] = np.mean(points, axis=0)

        # mam original_points z moim punktem - dict; faces z jedym zapełnionym facem;

        face_edges = []

        # go through all the edges of the face
        # edge = []
        for i in range(-1, np.size(cell_position)-1):
            edge = [cell_position[i], cell_position[i+1]]
            edge.sort()
            edge = tuple(edge)
            edge_object = {
                'points': [],
                'faces': []
            }
            if edge not in edges.keys():
                edge_object['points'].append(original_points[edge[0]])
                edge_object['points'].append(original_points[edge[1]])
                edges[edge] = edge_object
            else:
                edge_object = edges[edge]

            ## every odege should know its adjacent faces
            edges[edge]['faces'].append(faces[cell_position])

            # ever point should know its adjacent edges
            points_of_the_edge = edges[edge]['points']
            points_of_the_edge[0]['edges'].append(edge_object)
            points_of_the_edge[1]['edges'].append(edge_object)

            face_edges.append(edge_object)

        faces[cell_position]['edges'] = face_edges

    # w tej chiwli mam original points z dict-point; faces z edges, points, face-point; edges gdzie edge to lista points i faców

# Compute the edge points and the midpoints of every edge

    for edge, edge_values in edges.items():

        count = 0
        sum_face_points = np.zeros(8)
        sum_end_points = np.zeros(8)

        for face in edge_values['faces']:
            sum_face_points += face['face_point']

        for point in edge_values['points']:
            sum_end_points += point['point']


        edges[edge]['edge_point'] = (sum_end_points + sum_end_points) / 4 # zadkładam, że 4 jet zawsze 4
        edges[edge]['mid_point'] = sum_end_points / 2

    # Each original point is moved to the position from the ecaution

    for i in range(vertices.shape[1]):
        point = original_points[i]
        n = len(point['faces'])

        length = 0
        q_value = np.zeros(8)
        for face in point['faces']:
            q_value += faces[face]['face_point']
            length = faces[face]['face_point'].shape[0]

        q_value = q_value / length

        num_of_edges = 0
        r_value = np.zeros(8)
        for edge in point['edges']:
            r_value += edge['mid_point']
            num_of_edges = edge['mid_point'].shape[0]

        r_value = r_value / num_of_edges

        new_point = q_value/num_of_edges + 2 * r_value / num_of_edges + (num_of_edges - 3) * point['point']
        point['new_point'] = new_point


    new_verticies = []
    new_cells = []
    index = 0
    used_points = []

    def check_if_conatins(array, list):
        for element in list:
            if np.array_equal(element, array):
                return True
        return False

    def get_index(point, index):
        if ( not check_if_conatins(point, new_verticies)):
            index += 1
            new_verticies.append(point)
        return index

    # We go through all faces

    for face in faces.values():
        for ind_point in range(len(face['points'])):
            point = face['points'][ind_point]
            len_edges = len(face['edges'])
            a = point['new_point']
            b = face['edges'][ind_point % len_edges]['edge_point']
            c = face['face_point']
            d = face['edges'][(ind_point + len_edges-1) % len_edges]['edge_point']

            ind_a = get_index(a, index)
            ind_b = get_index(b, index)
            ind_c = get_index(c, index)
            ind_d = get_index(d, index)
            new_cells.append([ind_a, ind_b, ind_c, ind_d])

    return (new_verticies, new_cells)

























#     face_points = []

#     for face in faces:
#         points = np.empty((np.size(face), 8))
#         for i, index in enumerate(face):
#             vertex = np.array(vertices[index])
#             points[i] = vertex
#         face_points.append(np.mean(points))

#     print(faces)
#     print('\n')
#     print(face_points)
#     print('\n')
#     print([list(row[:3]) for row in vertices])

#     edge_points = []
#     get_neighbour(faces, face_points, vertices)
#     return (vertices, faces)

# def get_neighbour(faces, face_points, vertices):
#     size = np.size(faces[0])
#     edges = [[(vertices[face[i]], vertices[face[i+1]]) for i in range(-1, np.size(faces[0])-1)] for face in faces]
#     pass


