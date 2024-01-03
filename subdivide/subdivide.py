#! /usr/bin/python

import cli
import model_io

import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


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
        glutMainLoop()

    def _init_opengl(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(os.path.basename(__file__))
        glutDisplayFunc(self._render_frame)

    def _render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutSwapBuffers()


if __name__ == "__main__":
    Application().run()
