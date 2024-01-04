#! /usr/bin/python

import cli
import mesh_io
import model

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import OpenGL.GL.shaders as shaders

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


class Application:
    def run(self):
        args = cli.parse_arguments()
        print(f"Model: {args.model_path}")
        print(f"Algorithm: {args.algorithm}")
        vertices, faces = mesh_io.load_model(args.model_path)
        print(f"Loaded {vertices.shape[0]} vertices and {faces.shape[0]} faces")
        print("Initialising OpenGL...")
        self._init_opengl()
        self.model = model.Model(self.shader, vertices, faces)
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
