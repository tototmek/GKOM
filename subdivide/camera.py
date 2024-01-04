import glm
from OpenGL.GLUT import *


class Camera:
    def __init__(self, position: glm.vec3, target: glm.vec3, up: glm.vec3):
        self._position = position
        self._target = target
        self._up = up

    def get_view_matrix(self):
        return glm.lookAt(self._position, self._target, self._up)

    def set_position(self, position: glm.vec3):
        self._position = position
        self._notify_redraw()

    def set_target(self, target: glm.vec3):
        self._target = target
        self._notify_redraw()

    def set_up(self, up: glm.vec3):
        self._up = up
        self._notify_redraw()

    def _notify_redraw(self):
        glutPostRedisplay()
