import numpy as np

def catmull_clark_subdivision(vertices, cells: np.array):
    print("Performing Catmull-Clark subdivision surface")

    original_points = {}
    faces = []
    edges = {}

    for ind_cell in range(np.size(cells)):

        cell_position = cells[ind_cell]
        faces.append({'points': [], 'face_point': None}) # for points and face_points) fejsy się nie powtarzają więc chyba jest git
        face_points = []

        for index in cell_position:
            if index in original_points.keys():
                v = vertices[index]

                point = {
                    'point': v,
                    'faces': [],
                    'edges': set()
                }
                original_points[index] = point # może tu coś się zjebało
            else:
                point = original_points[index]

            # Now point has a reference to its face
            point['faces'].append(cell_position)
            face_points.append(point)

        faces[ind_cell]['points'] = face_points

        ## getting the facepoint

        points = np.empty((np.size(cell_position), 8))
        for i, index in enumerate(cell_position):
            vertex = np.array(vertices[index])
            points[i] = vertex

        faces[ind_cell]['face_point'] = np.mean(points)

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
            if edge in edges.keys():
                edge_object['points'].append(original_points[edge[0]])
                edge_object['points'].append(original_points[edge[1]])
                edges[edge] = edge_object
            else:
                edge_object = edges[edge]

            ## every odege should know its adjacent faces
            edges[edge]['faces'].append(faces[ind_cell])

            # ever point should know its adjacent edges
            points_of_the_edge = edges[edge]['points']
            points_of_the_edge[0]['edges'].add(edge_object)
            points_of_the_edge[1]['edges'].add(edge_object)

            face_edges.append(edge_object)

        faces[ind_cell]['edges'] = face_edges

    # w tej chiwli mam original points z dict-point; faces z edges, points, face-point; edges gdzie edge to lista points i faców

# Compute the edge points and the midpoints of every edge

    for edge in edges:

        count = 0
        sum_face_points = np.zeros(3)
        sum_end_points = np.zeros(3)

        for face in edge['faces']:
            sum_face_points += face['face_point']

        for point in edge['points']:
            sum_end_points += points['point']


        edge['edge_point'] = (sum_end_points + sum_end_points) / 4 # zadkładam, że 4 jet zawsze 4
        edge['mid_point'] = sum_end_points / 2

























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


