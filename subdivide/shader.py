from OpenGL.GL import *
import OpenGL.GL.shaders as shaders


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
        vertex_source = load_file_as_string(vertex_shader_path)
        fragment_source = load_file_as_string(fragment_shader_path)
        self.program = shaders.compileProgram(
            shaders.compileShader(vertex_source, GL_VERTEX_SHADER),
            shaders.compileShader(fragment_source, GL_FRAGMENT_SHADER),
        )
