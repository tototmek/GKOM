from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import glm
import numpy


def load_file_as_string(file_path):
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error while reading file '{file_path}': {e}")
        exit(1)


class Shader:
    def __init__(self, vertex_shader_path, fragment_shader_path):
        vertex = load_file_as_string(vertex_shader_path)
        fragment = load_file_as_string(fragment_shader_path)
        self._compile_source(vertex, fragment)
        self._setup_uniforms()

    def use(self):
        glUseProgram(self.program)

    def set_uniform_mat4(self, uniform_name, value: glm.mat4):
        if self._is_uniform_unknown(uniform_name):
            return
        location = self.uniform_locations[uniform_name]
        glUniformMatrix4fv(location, 1, GL_TRUE, numpy.array(value))

    def set_uniform_vec3(self, uniform_name, value: glm.vec3):
        if self._is_uniform_unknown(uniform_name):
            return
        location = self.uniform_locations[uniform_name]
        glUniform3fv(location, 1, glm.value_ptr(value))

    def set_uniform_int(self, uniform_name, value: int):
        if self._is_uniform_unknown(uniform_name):
            return
        location = self.uniform_locations[uniform_name]
        glUniform1i(location, value)

    def _is_uniform_unknown(self, uniform_name):
        return not uniform_name in self.uniform_locations

    def _compile_source(self, vertex_source, fragment_source):
        self.program = shaders.compileProgram(
            shaders.compileShader(vertex_source, GL_VERTEX_SHADER),
            shaders.compileShader(fragment_source, GL_FRAGMENT_SHADER),
        )

    def _setup_uniforms(self):
        self.uniform_types = {}
        self.uniform_locations = {}
        uniform_count = glGetProgramiv(self.program, GL_ACTIVE_UNIFORMS)
        for i in range(uniform_count):
            uniform_info = glGetActiveUniform(self.program, i)
            uniform_name = uniform_info[0].decode()
            uniform_location = glGetUniformLocation(self.program, uniform_name)
            self.uniform_locations[uniform_name] = uniform_location
