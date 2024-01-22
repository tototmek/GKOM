import pyassimp
import os
import numpy
import pywavefront

def read_file(path):
    faces = []
    with open(path, 'r') as file:
        for line in file:
            if line[0] == 'f':
                points = line[2:-1].split(' ')
                for point in points:
                    indexes = point.split('/')
                    indexes = [int(i) for i in indexes]
                    faces.append(indexes)
    return faces

def load_using_wave(path):
    scene =  pywavefront.Wavefront(path, strict=True, collect_faces=True)
    verticies = numpy.array(scene.vertices)
    normals = numpy.array(scene.parser.normals)
    textures_coords = numpy.array(scene.parser.tex_coords)

    faces = read_file(path)

    verticies_all = numpy.zeros((len(faces), 8))

    for i, face in enumerate(faces):
        verticies_all[i] = numpy.concatenate((verticies[face[0]-1], normals[face[2]-1], textures_coords[face[1]-1]))
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15],
        [16, 17, 18, 19],
        [20, 21, 22, 23]
    ]
    verticies = verticies_all[:, 0:3]

    new_verticies, new_faces = get_proper_faces(verticies, numpy.array(faces))
    # vertices = numpy.hstack((numpy.array(new_verticies), normals, textures_coords))

    return (numpy.array(new_verticies), numpy.array(new_faces))



def load_using_assimp(path):
    with pyassimp.load(path, processing=pyassimp.postprocess.aiProcess_JoinIdenticalVertices) as scene:
        if len(scene.meshes) == 0:
            print("Warning: Empty mesh")
            return ([], [])
        mesh = scene.meshes[0]

        if len(mesh.texturecoords) < 1:
            print("Error: Mesh does not contain texture coordinates")
            exit(1)

        positions = numpy.array(mesh.vertices, dtype=numpy.float32)
        normals = numpy.array(mesh.normals, dtype=numpy.float32)
        tex_coords = numpy.array(mesh.texturecoords[0], dtype=numpy.float32)
        tex_coords = tex_coords[:, :2]
        # normals = numpy.full((positions.shape[0], 3), 0.5)
        vertices = numpy.hstack((positions, normals, tex_coords))
        faces = numpy.array(mesh.faces, dtype=numpy.uint32)
        return (vertices, faces)


model_loaders = {
    "obj": load_using_wave,
    "stl": load_using_assimp,
    "ply": load_using_assimp,
}


def load_model(path):
    file_extension = os.path.splitext(path)[1][1:].lower()
    return model_loaders[file_extension](path)


def get_proper_faces(verticies, faces):
    new_faces = []
    new_verticies = []
    face_index = 0
    for j, face in enumerate(faces):
        new_faces.append([])
        for i, index in enumerate(face):
            vert_ind = position(new_verticies, verticies, index)
            if (vert_ind == -1):
                new_verticies.append(verticies[index])
                new_faces[j].append(face_index)

                face_index += 1
            else:
                new_faces[j].append(vert_ind)
    return new_verticies, new_faces


            
def position(new_verticies, verticies, index):
    for i in range(len(new_verticies)):
        if numpy.array_equal(new_verticies[i], verticies[index]):
           return i
    return -1       