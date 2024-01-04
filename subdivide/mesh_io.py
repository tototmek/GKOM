import pyassimp
import os
import numpy


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
