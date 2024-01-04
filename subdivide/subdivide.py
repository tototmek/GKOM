#! /usr/bin/python

import cli
import mesh_io
import model
import shader
import environment
import camera

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import glm


def mouse_callback(button, state, x, y):
    print(f"Mouse button {button} {state} at ({x}, {y})")


def motion_callback(x, y):
    print(f"Mouse position: ({x}, {y})")


class Application:
    def run(self):
        args = cli.parse_arguments()
        self.render_wireframe = args.wireframe
        print(f"Model: {args.model_path}")
        print(f"Algorithm: {args.algorithm}")
        vertices, faces = mesh_io.load_model(args.model_path)
        print(f"Loaded {vertices.shape[0]} vertices and {faces.shape[0]} faces")
        print("Initialising OpenGL...")
        self._init_opengl()
        self.object_shader = shader.Shader(
            "assets/shaders/basic.vert", "assets/shaders/basic.frag"
        )
        self.wireframe_shader = shader.Shader(
            "assets/shaders/basic.vert", "assets/shaders/wireframe.frag"
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
        glutMouseFunc(mouse_callback)
        glutMotionFunc(motion_callback)
        glClearColor(0.12, 0.12, 0.12, 1.0)
        glLineWidth(2.0)
        glEnable(GL_DEPTH_TEST)

    def _render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cam = camera.Camera(
            glm.vec3(-2.0, -8.0, 2.0), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 0.0, 1.0)
        )

        scene = environment.Environment()
        scene.view_matrix = cam.get_view_matrix()
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

        self.model.draw(self.object_shader, scene)
        if self.render_wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            self.model.draw(self.wireframe_shader, scene)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glutSwapBuffers()

        print("Rendered")


if __name__ == "__main__":
    Application().run()
