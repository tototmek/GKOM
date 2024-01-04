#! /usr/bin/python

import cli
import mesh_io
import model
import shader
import environment

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

        camera_position = glm.vec3(-2.0, -8.0, 2.0)
        target_position = glm.vec3(0.0, 0.0, 0.0)

        scene = environment.Environment()
        scene.view_matrix = glm.lookAt(
            camera_position, target_position, glm.vec3(0.0, 0.0, 1.0)
        )
        scene.projection_matrix = glm.perspective(
            glm.radians(45.0), 640.0 / 480.0, 0.1, 100.0
        )
        scene.light = environment.Light()
        scene.light.position = glm.vec3(-5.0, -2.0, 5.0)
        scene.light.ambient = glm.vec3(0.2, 0.2, 0.2)
        scene.light.diffuse = glm.vec3(1.0, 1.0, 1.0)
        scene.light.specular = glm.vec3(1.0, 1.0, 1.0)
        scene.material_diffuse = glm.vec3(0.1, 0.4, 0.2)
        scene.material_specular = glm.vec3(1.0, 1.0, 1.0)

        self.model.draw(self.shader, scene)
        glutSwapBuffers()


if __name__ == "__main__":
    Application().run()
