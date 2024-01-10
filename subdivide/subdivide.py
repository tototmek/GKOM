#! /usr/bin/python

import cli
import mesh_io
import model
import shader
import environment
import camera
import mouse_camera_controller
import loop_subdivision
import catmull_clark_subdivision
import subdivision_proxy

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import glm


class Application:
    def run(self):
        args = cli.parse_arguments()
        self.render_wireframe = args.wireframe
        print(f"Model: {args.model_path}")
        print(f"Algorithm: {args.algorithm}")
        algorithm_function = (
            loop_subdivision.loop_subdivision
            if args.algorithm == "loop"
            else catmull_clark_subdivision.catmull_clark_subdivision
        )
        vertices, faces = mesh_io.load_model(args.model_path)
        print(f"Loaded {vertices.shape[0]} vertices and {faces.shape[0]} faces")
        print("Initialising OpenGL...")
        self._init_opengl()

        self.subdivisions = subdivision_proxy.SubdivisionProxy(
            algorithm_function, vertices, faces, 4
        )
        self.model = self.subdivisions.get_current_model()
        self.object_shader = shader.Shader(
            "assets/shaders/basic.vert", "assets/shaders/basic.frag"
        )
        self.wireframe_shader = shader.Shader(
            "assets/shaders/basic.vert", "assets/shaders/wireframe.frag"
        )
        self.cam = camera.Camera(
            glm.vec3(-2.0, -8.0, 2.0), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 0.0, 1.0)
        )
        self.camera_controller = mouse_camera_controller.MouseCameraController(self.cam)
        self.camera_controller.activate()
        glutMainLoop()

    def keyboard_handler(self, key, x, y):
        if key == b"w":
            self.model = self.subdivisions.get_next_model()
        elif key == b"s":
            self.model = self.subdivisions.get_previous_model()
        glutPostRedisplay()

    def _init_opengl(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(os.path.basename(__file__))
        glutDisplayFunc(self._render_frame)
        glutKeyboardFunc(self.keyboard_handler)
        glClearColor(0.12, 0.12, 0.12, 1.0)
        glLineWidth(2.0)
        glEnable(GL_DEPTH_TEST)

    def _render_frame(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        scene = environment.Environment()
        scene.view_matrix = self.cam.get_view_matrix()
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


if __name__ == "__main__":
    Application().run()
