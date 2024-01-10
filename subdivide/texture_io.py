from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import numpy


def read_texture(filename):
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        img.size[0],
        img.size[1],
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        img_data,
    )
    return texture_id


def generate_white_texture():
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    img_data = numpy.array([255 for _ in range(100 * 4)], numpy.int8)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        10,
        10,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        img_data,
    )
    return texture_id
