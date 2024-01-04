#! /usr/bin/python

import cli
import mesh_io
import model
import shader

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import glm


class Application:
    def run(self):
        args = cli.parse_arguments()
        print(f"Model: {args.model_path}")
        print(f"Algorithm: {args.algorithm}")
        vertices, faces = mesh_io.load_model(args.model_path)
        print(f"Loaded {vertices.shape[0]} vertices and {faces.shape[0]} faces")
        print("Initialising OpenGL...")
        self._init_opengl()
        self.shader = shader.Shader(
            "assets/shaders/basic.vert", "assets/shaders/basic.frag"
        )
        self.model = model.Model(vertices, faces)
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

    def _render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.model.draw(self.shader)
        glutSwapBuffers()


if __name__ == "__main__":
    Application().run()
