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

    return (verticies_all, numpy.array(faces))



def load_using_assimp(path):
    with pyassimp.load(path) as scene:
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
        print(normals)

        vertices = numpy.hstack((positions, normals, tex_coords))
        faces = numpy.array(mesh.faces, dtype=numpy.uint32)
        return (vertices, faces)


model_loaders = {
    "obj": load_using_assimp,
    "stl": load_using_assimp,
    "ply": load_using_assimp,
}


def load_model(path):
    file_extension = os.path.splitext(path)[1][1:].lower()
    return model_loaders[file_extension](path)
