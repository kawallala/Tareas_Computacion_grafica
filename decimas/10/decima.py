# coding=utf-8

import sys
from math import sqrt

import glfw
import numpy as np
import OpenGL.GL.shaders
from OpenGL.GL import *

import basic_shapes as bs
import easy_shaders as es
import scene_graph2 as sg
import transformations2 as tr2
from ex_curves import evalCurve, hermiteMatrix


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.camera = 0
        self.texture = True

        # change this to True for TRUE fun
        self.ricardo = False


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    # keys to use to determine the camera to use
    if key == glfw.KEY_1:
        controller.camera = 0

    if key == glfw.KEY_2:
        controller.camera = 1

    if key == glfw.KEY_3:
        controller.camera = 2

    if key == glfw.KEY_4:
        controller.camera = 3

    if key == glfw.KEY_5:
        controller.camera = 4

    if key == glfw.KEY_R:
        controller.ricardo = not controller.ricardo

    elif key == glfw.KEY_ESCAPE:
        sys.exit()


def create_sphere():
    # parametres to use for the 2 curves used
    N = 10

    P1_1 = np.array([[0, 0, -1]]).T
    P2_1 = np.array([[0, 0, 1]]).T
    T1_1 = np.array([[4, 0, 0]]).T
    T2_1 = np.array([[-4, 0, 0]]).T

    GMh = hermiteMatrix(P1_1, P2_1, T1_1, T2_1)

    hermiteCurve_1 = evalCurve(GMh, N)

    # depending on the controller value, we create objects with or without textures
    if controller.texture:
        gpuCurve_1 = es.toGPUShape(
            bs.createTextureCurve(hermiteCurve_1, 0, 1, "mapa.jpg"),
            GL_CLAMP_TO_EDGE,
            GL_LINEAR,
        )
    else:
        gpuCurve_1 = es.toGPUShape(bs.createColorCurve(hermiteCurve_1, 0, 0, 1))

    curve_1 = sg.SceneGraphNode("curve_1")
    curve_1.transform = tr2.identity()
    curve_1.childs += [gpuCurve_1]

    curve = sg.SceneGraphNode("building")
    curve.childs += [curve_1]

    return curve


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Projections Demo", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program
    if controller.texture:
        pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    else:
        pipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0, 0, 0, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))

    curve = create_sphere()

    t0 = glfw.get_time()
    camera_theta = np.pi / 2
    camera_phi = np.pi / 2
    camera_radius = 2
    camera_height = 0
    up_vector = np.array([0, 0, 1])
    inverse = 1
    t_ascensor = 0

    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        t_ascensor += dt / 2
        if controller.camera == 0:
            if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
                camera_theta -= dt

            if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
                camera_theta += dt

            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
                camera_phi -= dt

            if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
                camera_phi += dt

            if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
                camera_radius -= dt

            if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
                camera_radius += dt

            if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
                camera_height += dt

            if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
                camera_height -= dt

            if camera_phi > np.pi:
                camera_phi = np.pi
            if camera_phi < 0:
                camera_phi = 0.0000000001

            # Setting up the view transform

            camX = camera_radius * np.sin(camera_phi) * np.cos(camera_theta)
            camY = camera_radius * np.sin(camera_phi) * np.sin(camera_theta)
            camZ = camera_radius * np.cos(camera_phi) + camera_height

            viewPos = np.array([camX, camY, camZ])

            view = tr2.lookAt(viewPos, [0, 0, camera_height], up_vector)

        if controller.camera == 1:

            view = tr2.lookAt(
                np.array([0.4, 0, 2.25 * np.sin(t_ascensor) + 3]),
                np.array([0, 0, 2.25 * np.sin(t_ascensor) + 3]),
                np.array([0, 0, 1]),
            )

        if controller.camera == 2:
            view = tr2.lookAt(
                np.array([4.0600955379233, 2.648779084987683, 0.12314699209696078]),
                np.array([0, 0, 2.0706694199539326]),
                np.array([0, 0, 1]),
            )

        if controller.camera == 3:
            view = tr2.lookAt(
                np.array([0.7954892298357678, 4.919143652269179, 7.992804633313877]),
                np.array([0, 0, 4.9690918315888695]),
                np.array([0, 0, 1]),
            )

        if controller.camera == 4:
            view = tr2.lookAt(
                np.array([0, -3, 3]), np.array([0, 0, 0]), np.array([0, 0, 1])
            )

        glUniformMatrix4fv(
            glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view
        )

        # Setting up the projection transform
        projection = tr2.perspective(60, float(width) / float(height), 0.1, 100)

        glUniformMatrix4fv(
            glGetUniformLocation(pipeline.shaderProgram, "projection"),
            1,
            GL_TRUE,
            projection,
        )

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        sg.drawSceneGraphNode(curve, pipeline)
        if not controller.texture:

            glUniformMatrix4fv(
                glGetUniformLocation(pipeline.shaderProgram, "model"),
                1,
                GL_TRUE,
                tr2.identity(),
            )

            pipeline.drawShape(gpuAxis, GL_LINES)
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
