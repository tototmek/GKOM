from camera import Camera
from OpenGL.GLUT import *
import glm
from math import sin, cos, acos, atan2, sqrt


class MouseCameraController:
    def __init__(
        self,
        cam: Camera,
        rotation_speed: glm.vec3 = glm.vec3(0.01, 0.01, 1),
        translation_speed: glm.vec3 = glm.vec3(0.01, 0.01, 0.01),
        start_pos: glm.vec3 = glm.vec3(3.14, 0.0, 8.0),
        start_target: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
    ):
        self.cam = cam
        self.position = start_pos
        self.target = start_target
        self.rotation_speed = rotation_speed
        self.translation_speed = translation_speed
        self.mode = 0

    def activate(self):
        glutMouseFunc(self.mouse_callback)
        glutMotionFunc(self.motion_callback)

    def mouse_callback(self, button, state, x, y):
        if button == 0 and state == 0:  # left pressed
            self.prev_x = x
            self.prev_y = y
            self.mode = 0
        if button == 1 and state == 0:  # scroll pressed
            self.prev_x = x
            self.prev_y = y
            self.mode = 1
        if button == 2 and state == 0:  # right pressed
            self.prev_x = x
            self.prev_y = y
            self.mode = 2
        if button == 3 and state == 0:  # scroll +
            self._move(
                glm.vec3(0.0, 0.0, self.rotation_speed.z),
                glm.vec3(0.0, 0.0, 0.0),
            )
        if button == 4 and state == 0:  # scroll -
            self._move(
                glm.vec3(0.0, 0.0, -self.rotation_speed.z),
                glm.vec3(0.0, 0.0, 0.0),
            )

    def motion_callback(self, x, y):
        dx = x - self.prev_x
        dy = y - self.prev_y
        self.prev_x = x
        self.prev_y = y
        if self.mode == 0:
            self._move(
                glm.vec3(-dx * self.rotation_speed.x, -dy * self.rotation_speed.y, 0.0),
                glm.vec3(0.0, 0.0, 0.0),
            )
        if self.mode == 1:
            self._move(
                glm.vec3(0.0, 0.0, 0.0),
                glm.vec3(
                    -dx * self.translation_speed.x, dy * self.translation_speed.y, 0.0
                ),
            )

    def _move(self, delta_pos: glm.vec3, delta_target: glm.vec3):
        camera_matrix = glm.inverse(self.cam.get_view_matrix())
        camera_up = glm.vec3(camera_matrix * glm.vec4(0.0, 1.0, 0.0, 0.0))
        camera_right = glm.vec3(camera_matrix * glm.vec4(1.0, 0.0, 0.0, 0.0))
        rotation_matrix = glm.rotate(
            glm.rotate(delta_pos.x, camera_up), delta_pos.y, camera_right
        )
        scaling_matrix = glm.scale(1.0 - glm.vec3(delta_pos.z) / self.position.z)
        camera_up = glm.vec3(rotation_matrix * glm.vec4(self.cam._up, 0.0))
        camera_position = glm.vec3(
            scaling_matrix * rotation_matrix * glm.vec4(self.cam._position, 0.0)
        )
        self.target += glm.vec3(camera_matrix * glm.vec4(delta_target, 0.0))
        self.cam.set_position(camera_position)
        self.cam.set_target(self.target)
        self.cam.set_up(camera_up)
        self.cam.notify_redraw()
