import pyassimp
import os
import numpy


def load_using_assimp(path):
    with pyassimp.load(path) as scene:
        if len(scene.meshes) == 0:
            return ([], [])
        mesh = scene.meshes[0]
        vertices = numpy.array(mesh.vertices, dtype=numpy.float32)
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
