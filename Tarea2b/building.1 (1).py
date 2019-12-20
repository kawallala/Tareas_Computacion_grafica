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
from ex_aux_4 import *
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


def create_skyBox():

    # by using the texture command in the controller, we use, or not textures for the objects used
    if controller.texture:
        if controller.ricardo:
            gpusky_1 = es.toGPUShape(
                bs.createTextureQuad("ricardo1.png"), GL_REPEAT, GL_NEAREST
            )
            gpusky_top = es.toGPUShape(
                bs.createTextureQuad("ricardo2.png"), GL_REPEAT, GL_NEAREST
            )
        else:
            gpusky_1 = es.toGPUShape(
                bs.createTextureQuad("city_2.jpg"), GL_REPEAT, GL_NEAREST
            )
            gpusky_top = es.toGPUShape(
                bs.createTextureQuad("sky_1.jpg"), GL_REPEAT, GL_NEAREST
            )
    else:
        gpusky_1 = es.toGPUShape(bs.createColorQuad(1, 0, 0))
        gpusky_top = es.toGPUShape(bs.createColorQuad(0, 1, 0))

    # creating the city around the building
    sky_1 = sg.SceneGraphNode("sky_1")
    sky_1.transform = tr2.matmul(
        [
            tr2.translate(5, 0, 5),
            tr2.rotationX(np.pi / 2),
            tr2.rotationY(np.pi / 2),
            tr2.uniformScale(10),
        ]
    )
    sky_1.childs += [gpusky_1]

    sky_2 = sg.SceneGraphNode("sky_2")
    sky_2.transform = tr2.rotationZ(np.pi / 2)
    sky_2.childs += [sky_1]

    sky_3 = sg.SceneGraphNode("sky_3")
    sky_3.transform = tr2.rotationZ(np.pi / 2)
    sky_3.childs += [sky_2]

    sky_4 = sg.SceneGraphNode("sky_4")
    sky_4.transform = tr2.rotationZ(np.pi / 2)
    sky_4.childs += [sky_3]

    # creating directly the sky
    sky_top = sg.SceneGraphNode("sky_top")
    sky_top.transform = tr2.matmul([tr2.translate(0, 0, 10), tr2.uniformScale(10)])
    sky_top.childs += [gpusky_top]

    sky = sg.SceneGraphNode("sky")
    sky.childs += [sky_1]
    sky.childs += [sky_2]
    sky.childs += [sky_3]
    sky.childs += [sky_4]
    sky.childs += [sky_top]

    return sky


def create_buildings():
    # parametres to use for the 2 curves used
    N = 10
    P1_1 = np.array([[0, 0, 0]]).T
    P2_1 = np.array([[0.05, 0, 0.1]]).T
    T1_1 = np.array([[1.8, 0, 0]]).T
    T2_1 = np.array([[-1.8, 0, 0]]).T

    GMh = hermiteMatrix(P1_1, P2_1, T1_1, T2_1)

    hermiteCurve_1 = evalCurve(GMh, N)

    P1_2 = np.array([[0.05, 0, 0.1]]).T
    P2_2 = np.array([[0, 0, 3]]).T
    T1_2 = np.array([[-0.0005, 0, 0]]).T
    T2_2 = np.array([[0, 0, 10]]).T

    GMh = hermiteMatrix(P1_2, P2_2, T1_2, T2_2)

    hermiteCurve_2 = evalCurve(GMh, N)

    # depending on the controller value, we create objects with or without textures
    if controller.texture:
        if controller.ricardo:
            gpuCurve_1 = es.toGPUShape(
                bs.createTextureCurve(hermiteCurve_1, 0, 0.5, "ricardo1.png"),
                GL_REPEAT,
                GL_NEAREST,
            )
            gpuCurve_2 = es.toGPUShape(
                bs.createTextureCurve(hermiteCurve_2, 0.5, 1, "ricardo1.png"),
                GL_REPEAT,
                GL_NEAREST,
            )
            gpuGround = es.toGPUShape(
                bs.createTextureQuad("ricardo2.png"), GL_REPEAT, GL_NEAREST
            )
            gpuCilinder = es.toGPUShape(
                bs.createTextureCilinderExtended(1, 1, "ricardo3.png"),
                GL_REPEAT,
                GL_NEAREST,
            )
        else:
            gpuCurve_1 = es.toGPUShape(
                bs.createTextureCurve(hermiteCurve_1, 0, 0.5, "ds.png"),
                GL_REPEAT,
                GL_NEAREST,
            )
            gpuCurve_2 = es.toGPUShape(
                bs.createTextureCurve(hermiteCurve_2, 0.5, 1, "ds.png"),
                GL_REPEAT,
                GL_NEAREST,
            )
            gpuGround = es.toGPUShape(
                bs.createTextureQuad("ground.jpg"), GL_REPEAT, GL_NEAREST
            )
            gpuCilinder = es.toGPUShape(
                bs.createTextureCilinderExtended(1, 1, "clock_3.jpg"),
                GL_REPEAT,
                GL_NEAREST,
            )
    else:
        gpuCurve_1 = es.toGPUShape(bs.createColorCurve(hermiteCurve_1, 0, 0, 1))
        gpuCurve_2 = es.toGPUShape(bs.createColorCurve(hermiteCurve_2, 0, 1, 0))
        gpuGround = es.toGPUShape(bs.createRainbowQuad())
        gpuCilinder = es.toGPUShape(bs.createColorCilinderExtended(1, 1, 1, 0, 0))

    # creating the ground for the building to stand on
    ground = sg.SceneGraphNode("Ground")
    ground.transform = tr2.uniformScale(10)
    ground.childs += [gpuGround]

    # creating two "clocks", however, ricardo's power twist them
    clock12 = sg.SceneGraphNode("clock12")
    # clock12.transform = tr2.translate(0,0,0.5)
    clock12.transform = tr2.matmul(
        [tr2.translate(0, 0, 1.5), tr2.rotationX(np.pi / 2), tr2.scale(0.1, 0.1, 0.8)]
    )
    clock12.childs += [gpuCilinder]

    clock34 = sg.SceneGraphNode("clocl34")
    clock34.transform = tr2.rotationZ(np.pi / 2)
    clock34.childs += [clock12]

    # creating all of the levels for the building
    level0 = sg.SceneGraphNode("level0")
    level0.transform = tr2.translate(0, 0, 0.5)

    level1 = sg.SceneGraphNode("level1")
    level1.transform = tr2.translate(0, 0, 2.000001)

    level2 = sg.SceneGraphNode("level2")
    level2.transform = tr2.translate(0, 0, 2.500000001)

    if controller.texture:
        if controller.ricardo:
            level0.childs += [
                es.toGPUShape(
                    bs.createTextureCubeExtended(1, 0.7, 1.5, "ricardo1.png"),
                    GL_REPEAT,
                    GL_NEAREST,
                )
            ]
            level1.childs += [
                es.toGPUShape(
                    bs.createTextureCubeExtended(0.7, 1, 0.5, "ricardo2.png"),
                    GL_REPEAT,
                    GL_NEAREST,
                )
            ]
            level2.childs += [
                es.toGPUShape(
                    bs.createTextureCubeExtended(0.7, 1, 0.5, "ricardo3.png"),
                    GL_REPEAT,
                    GL_NEAREST,
                )
            ]
        else:
            level0.childs += [
                es.toGPUShape(
                    bs.createTextureCubeExtended(1, 0.7, 1.5, "windows_1.png"),
                    GL_REPEAT,
                    GL_NEAREST,
                )
            ]
            level1.childs += [
                es.toGPUShape(
                    bs.createTextureCubeExtended(0.7, 1, 0.5, "windows_4.jpg"),
                    GL_REPEAT,
                    GL_NEAREST,
                )
            ]
            level2.childs += [
                es.toGPUShape(
                    bs.createTextureCubeExtended(0.7, 1, 0.5, "windows_3.jpg"),
                    GL_REPEAT,
                    GL_NEAREST,
                )
            ]
    else:
        level0.childs += [
            es.toGPUShape(
                bs.createColorCubeExtended(
                    1, 0.7, 1.5, 128 / 255.0, 177 / 255.0, 194 / 255.0
                )
            )
        ]
        level1.childs += [
            es.toGPUShape(
                bs.createColorCubeExtended(
                    0.7, 1, 0.5, 128 / 255.0, 177 / 255.0, 194 / 255.0
                )
            )
        ]
        level2.childs += [
            es.toGPUShape(
                bs.createColorCubeExtended(
                    0.7, 1, 0.5, 128 / 255.0, 177 / 255.0, 194 / 255.0
                )
            )
        ]

    level3 = sg.SceneGraphNode("level3")
    level3.transform = tr2.translate(0, 0, 1)
    level3.childs += [level1]

    level4 = sg.SceneGraphNode("level4")
    level4.transform = tr2.translate(0, 0, 1)
    level4.childs += [level2]

    level5 = sg.SceneGraphNode("level5")
    level5.transform = tr2.translate(0, 0, 1)
    level5.childs += [level3]

    level6 = sg.SceneGraphNode("level6")
    level6.transform = tr2.translate(0, 0, 1)
    level6.childs += [level4]

    level7 = sg.SceneGraphNode("level7")
    level7.transform = tr2.translate(0, 0, 1)
    level7.childs += [level5]

    level8 = sg.SceneGraphNode("level8")
    level8.transform = tr2.translate(0, 0, 1)
    level8.childs += [level6]

    curve_1 = sg.SceneGraphNode("curve_1")
    curve_1.transform = tr2.translate(0, 0, 5.5)
    curve_1.childs += [gpuCurve_1]

    curve_2 = sg.SceneGraphNode("curve_2")
    curve_2.transform = tr2.translate(0, 0, 5.5)
    curve_2.childs += [gpuCurve_2]

    building = sg.SceneGraphNode("building")

    building.childs += [ground]
    building.childs += [level0]
    building.childs += [level1]
    building.childs += [level2]
    building.childs += [level3]
    building.childs += [level4]
    building.childs += [level5]
    building.childs += [level6]
    building.childs += [level7]
    building.childs += [level8]
    building.childs += [clock12]
    building.childs += [clock34]
    building.childs += [curve_1]
    building.childs += [curve_2]

    return building


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

    building = create_buildings()
    skyBox = create_skyBox()

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

        sg.drawSceneGraphNode(building, pipeline)
        sg.drawSceneGraphNode(skyBox, pipeline)
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
