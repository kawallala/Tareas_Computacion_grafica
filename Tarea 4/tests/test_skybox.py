# imports necessary for use
import glfw
from OpenGL.GL import *
from lib.mathlib import Point3
import sys

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph2 as sg
import lib.transformations2 as tr2
import lib.camera as cam
import lib.wireframe as wire
import lib.skybox as sky
import numpy as np

import lib.basic_shapes_extended as bs_ext
import lib.lights as light


class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.current_body_part = 0
        self.angle = 0
        self.firstPerson = False
        self.selectedKeyFrame = 0
        self.moving_allowed = True


controller = Controller()

# Create camera
camera = cam.CameraR(r=3)
camera.set_r_vel(0.1)
sky = sky.skybox()


def on_key(window_obj, key, scancode, action, mods):
    global controller

    if action == glfw.REPEAT or action == glfw.PRESS:
        # Move the camera position
        if key == glfw.KEY_A:
            camera.rotate_phi(-4)
        elif key == glfw.KEY_D:
            camera.rotate_phi(4)
        elif key == glfw.KEY_W:
            camera.rotate_theta(-4)
        elif key == glfw.KEY_S:
            camera.rotate_theta(4)
        elif key == glfw.KEY_Q:
            camera.close()
        elif key == glfw.KEY_E:
            camera.far()
        elif key == glfw.KEY_X:
            controller.firstPerson = not controller.firstPerson
        elif key == glfw.KEY_V:
            controller.angle += 0.06
        elif key == glfw.KEY_B:
            controller.angle -= 0.06
        elif key == glfw.KEY_Z:
            controller.angle = 0

        # Move the center of the camera
        elif key == glfw.KEY_I:
            camera.move_center_x(-0.05)
        elif key == glfw.KEY_K:
            camera.move_center_x(0.05)
        elif key == glfw.KEY_J:
            camera.move_center_y(-0.05)
        elif key == glfw.KEY_L:
            camera.move_center_y(0.05)
        elif key == glfw.KEY_U:
            camera.move_center_z(-0.05)
        elif key == glfw.KEY_O:
            camera.move_center_z(0.05)

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, "Tarea_4", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Create shader programs
    texturePipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    glUseProgram(texturePipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need t check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Create Axis
    gpuAxis = es.toGPUShape(bs.createAxis(1))

    # Create the skybox
    obj_skybox = sky.create_skybox()

    # Main execution loop
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state

        # Create projection
        projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)

        # Get camera view matrix
        view = camera.get_view()

        # Draw objects

        glUniformMatrix4fv(
            glGetUniformLocation(colorShaderProgram.shaderProgram, "view"),
            1,
            GL_TRUE,
            view,
        )
        glUniformMatrix4fv(
            glGetUniformLocation(colorShaderProgram.shaderProgram, "projection"),
            1,
            GL_TRUE,
            projection,
        )

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # glUseProgram(texturePipeline.shaderProgram)
        colorShaderProgram.drawShape(gpuAxis, GL_LINES)
        # glUseProgram(texturePipeline.shaderProgram)
        sg.drawSceneGraphNode(obj_skybox, texturePipeline)
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen
        glfw.swap_buffers(window)
    glfw.terminate()
