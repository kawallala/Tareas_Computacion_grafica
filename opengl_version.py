# coding=utf-8
"""
Sample code to determine OpenGL version available on this machine.
"""

import glfw
from OpenGL.GL import *
import sys


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    window = glfw.create_window(1, 1, "OpenGL versions", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    print("GPU                      : ", glGetString(GL_VENDOR))
    print("Renderer                 : ", glGetString(GL_RENDERER))
    print("OpenGL                   : ", glGetString(GL_VERSION))
    print("Shading Language Version : ", glGetString(GL_SHADING_LANGUAGE_VERSION))

    glfw.terminate()