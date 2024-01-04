#! /usr/bin/python

import cli
import model_io

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import OpenGL.GL.shaders as shaders
import numpy

vertex_shader = """
#version 330
in vec4 position;
void main()
{
   gl_Position = position;
}
"""

fragment_shader = """
#version 330
void main()
{
   gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""


def initialize_object(shader, vertices: numpy.ndarray, faces: numpy.ndarray):
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, sys.getsizeof(vertices), vertices, GL_STATIC_DRAW)

    face_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, face_buffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sys.getsizeof(faces), faces, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))

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


class Application:
    def run(self):
        args = cli.parse_arguments()
        print(f"Model: {args.model_path}")
        print(f"Algorithm: {args.algorithm}")
        print("Loading model...")
        vertices, faces = model_io.load_model(args.model_path)
        print(vertices)
        print(faces)
        print("Initialising OpenGL...")
        self._init_opengl()
        self.model = Model(self.shader, vertices, faces)
        glutMainLoop()

    def _init_opengl(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(os.path.basename(__file__))
        glutDisplayFunc(self._render_frame)

        glClearColor(0.12, 0.12, 0.12, 1.0)
        glEnable(GL_DEPTH_TEST)
        self.shader = shaders.compileProgram(
            shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER),
        )

    def _render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.model.draw()
        glutSwapBuffers()


if __name__ == "__main__":
    Application().run()
