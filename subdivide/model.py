from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import numpy
import sys


def initialize_object(shader, vertices: numpy.ndarray, faces: numpy.ndarray):
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
    position = glGetAttribLocation(shader, "position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))
    # Unbind everything
    glBindVertexArray(0)
    glDisableVertexAttribArray(position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vertex_array_object


class Model:
    def __init__(
        self,
        shader: shaders.ShaderProgram,
        vertices: numpy.ndarray,
        faces: numpy.ndarray,
    ):
        self.shader = shader
        self.vertices = vertices
        self.faces = faces
        self._vertex_array_object = initialize_object(shader, vertices, faces)

    def draw(self):
        glUseProgram(self.shader)
        glBindVertexArray(self._vertex_array_object)
        glDrawElements(GL_TRIANGLES, self.faces.size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glUseProgram(0)
