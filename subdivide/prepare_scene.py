import pyassimp
import numpy as np
import catmull_clark_subdivision


def create_scene(vertices, faces):

    scene = {'meshes': [], 'rootnode': {'children': []}}

    # Create a mesh
    mesh = {'vertices': np.array(vertices, dtype=np.float32)}

   
    # Create triangles from faces
    mesh['faces'] = np.array(faces, dtype=np.uint32)

    # Add the mesh to the scene
    scene['meshes'].append(mesh)

    # Create a node and attach the mesh to it
    node = {'meshes': [0]}  # Index of the mesh in the scene's mesh list
    scene['rootnode']['children'].append(node)

    # Calculate smooth normals
    pyassimp.postprocess.calc_smooth_normals(scene)
    # Calculate smooth normals
    pyassimp.postprocess.calc_smooth_normals(scene)

    mesh = scene.meshes[0]

       

    positions = np.array(mesh.vertices, dtype=np.float32)
    normals = np.array(mesh.normals, dtype=np.float32)
    tex_coords = np.array(mesh.texturecoords[0], dtype=np.float32)
    tex_coords = tex_coords[:, :2]
    # normals = np.full((positions
    vertices = np.hstack((positions, normals, tex_coords))
    faces = np.array(mesh.faces, dtype=np.uint32)
    return (vertices, faces)

def load_normals_and_textures(vertices, faces):
    export_file_row(vertices, faces)
    return load_trans_file('transformativ_file.obj')


def export_file(vertices, faces):
    scene = {'meshes': [], 'rootnode': {'children': []}}

    # Create a mesh
    mesh = {'vertices': np.array(vertices, dtype=np.float32)}

   
    # Create triangles from faces
    mesh['faces'] = np.array(faces, dtype=np.uint32)

    # Add the mesh to the scene
    scene['meshes'].append(mesh)

    # Create a node and attach the mesh to it
    node = {'meshes': [0]}  # Index of the mesh in the scene's mesh list
    scene['rootnode']['children'].append(node)

    pyassimp.export(scene, 'transformativ_file', 'obj', processing=pyassimp.postprocess.aiProcess_GenNormals)

def export_file_row(vertices, faces):
    filepath = "transformativ_file.obj"

   
    with open(filepath, 'w') as f:
        f.write("# OBJ file\n")
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for p in faces:
            f.write("f")
            for i in p:
                f.write(" %d" % (i + 1))
            f.write("\n")

def load_trans_file(path):
    with pyassimp.load(path, processing=pyassimp.postprocess.aiProcess_GenNormals) as scene:
        if len(scene.meshes) == 0:
            print("Warning: Empty mesh")
            return ([], [])
        mesh = scene.meshes[0]

        # if len(mesh.texturecoords) < 1:
        #     print("Error: Mesh does not contain texture coordinates")
        #     exit(1)

        positions = np.array(mesh.vertices, dtype=np.float32)
        normals = np.array(mesh.normals, dtype=np.float32)
        # tex_coords = np.array(mesh.texturecoords[0], dtype=np.float32)
        # tex_coords = tex_coords[:, :2]
        tex_coords = np.full((positions.shape[0], 3), 0.5)
        vertices = np.hstack((positions, normals, tex_coords))
        faces = np.array(mesh.faces, dtype=np.uint32)
        return (np.array(vertices), np.array(faces))