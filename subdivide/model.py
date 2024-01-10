from OpenGL.GL import *
from shader import Shader
from environment import Environment
import numpy
import sys
import glm


def initialize_object(vertices: numpy.ndarray, faces: numpy.ndarray):
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)
    # Create vertex buffer containing vertex data
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(vertices), vertices, GL_STATIC_DRAW)
    # Create face buffer containing vertex indices
    face_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, face_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sys.getsizeof(faces), faces, GL_STATIC_DRAW)
    # Setup vertex attribute locations
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        False,
        8 * sizeof(ctypes.c_float),
        ctypes.c_void_p(0 * sizeof(ctypes.c_float)),
    )
    glVertexAttribPointer(
        1,
        3,
        GL_FLOAT,
        False,
        8 * sizeof(ctypes.c_float),
        ctypes.c_void_p(3 * sizeof(ctypes.c_float)),
    )
    glVertexAttribPointer(
        2,
        2,
        GL_FLOAT,
        False,
        8 * sizeof(ctypes.c_float),
        ctypes.c_void_p(6 * sizeof(ctypes.c_float)),
    )
    # Unbind everything
    glBindVertexArray(0)
    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glDisableVertexAttribArray(2)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    return vertex_array_object


class Model:
    def __init__(
        self,
        vertices: numpy.ndarray,
        faces: numpy.ndarray,
    ):
        self.vertices = vertices
        self.faces = faces
        self._vertex_array_object = initialize_object(vertices, faces)
        self.model_matrix = glm.mat4(1.0)

    def draw(self, shader: Shader, environment: Environment):
        shader.use()
        shader.set_uniform_mat4("model", self.model_matrix)
        shader.set_uniform_mat4("view", environment.view_matrix)
        shader.set_uniform_mat4("projection", environment.projection_matrix)

        # Solid color
        # shader.set_uniform_vec3("material_diffuse", environment.material_diffuse)
        # shader.set_uniform_vec3("material_specular", environment.material_specular)

        # Texture
        shader.set_uniform_int("material_diffuse", 0)
        shader.set_uniform_int("material_specular", 1)

        shader.set_uniform_vec3("light_position", environment.light.position)
        shader.set_uniform_vec3("light_ambient", environment.light.ambient)
        shader.set_uniform_vec3("light_diffuse", environment.light.diffuse)
        shader.set_uniform_vec3("light_specular", environment.light.specular)

        glBindVertexArray(self._vertex_array_object)
        glDrawElements(GL_TRIANGLES, self.faces.size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
