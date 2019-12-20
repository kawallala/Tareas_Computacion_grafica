# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Drawing a car via a scene graph
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import scene_graph as sg
import sys

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


def createQuad(r, g, b):

    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape    
    vertexData = np.array([
    #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
         0.5, -0.5, 0.0,  r, g, b,
         0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


def createTriangle(r, g, b):

    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
    #   positions        colors
        -0.5,  0.0, 0.0,  r, g, b,
         0.5,  0.0, 0.0,  r, g, b,
         0.0,  0.5, 0.0,  r, g, b,
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         ], dtype= np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    # Vertex data must be attached to a Vertex Buffer Object (VBO)
    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) * INT_BYTES, vertexData, GL_STATIC_DRAW)

    # Connections among vertices are stored in the Elements Buffer Object (EBO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * INT_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape


def createForest():

    #creating the sky
    sky = sg.SceneGraphNode("sky")
    sky.transform = tr.uniformScale(2)
    sky.childs += [createQuad(25 / 255.0, 158 / 255.0, 218 / 255.0)]

    #creating the ground
    ground = sg.SceneGraphNode("ground")
    ground.transform = tr.matmul([tr.uniformScale(2),tr.translate(0.0,-1.0,0.0)])
    ground.childs += [createQuad(158/255.0, 219/255.0, 26/255.0)]

    # Creating a single trunk
    trunk = sg.SceneGraphNode("trunk")
    trunk.transform = tr.matmul([tr.scale(0.1,0.2,0.2),tr.translate(0.0,-0.25,0.0)])
    trunk.childs += [createQuad(80/255.0,55/255.0,22/255.0)]

    # Creating leaves
    leaves = sg.SceneGraphNode("leaves")
    leaves.transform = tr.matmul([tr.scale(0.3,1.0,1.0),tr.translate(0.0,-0.15,0.0)])
    leaves.childs += [createTriangle(30/255.0,147/255.0,47/255.0)]

    #moving the leaves
    leaves_wind = sg.SceneGraphNode("wind")
    leaves_wind.childs +=[leaves]

    #creating a tree
    tree = sg.SceneGraphNode("tree")
    tree.childs += [leaves_wind]
    tree.childs += [trunk]

    #second tree
    tree_2 = sg.SceneGraphNode("second tree")
    tree_2.transform = tr.translate(0.5,0.1,0)
    tree_2.childs += [tree]

    #third tree
    tree_3 = sg.SceneGraphNode("third tree")
    tree_3.transform = tr.matmul([tr.translate(-0.4,-0.3,0.0),tr.scale(0.7,1.3,0.0)])
    tree_3.childs += [tree]

    # BIG FUCKING TREE
    tree_big = sg.SceneGraphNode("big tree")
    tree_big.transform = tr.matmul([tr.translate(-0.3,0.2,0.0),tr.scale(2,2,0.0)])
    tree_big.childs +=[tree]

    #constructing the forest
    forest = sg.SceneGraphNode("forest")
    forest.childs += [sky]
    forest.childs += [ground]
    forest.childs += [tree]
    forest.childs += [tree_2]
    forest.childs += [tree_3]
    forest.childs += [tree_big]

    return forest


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Drawing a Quad via a EBO", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = sg.basicShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Creating shapes on GPU memory
    forest = createForest()

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Modifying the wind node
        leavesWindNode = sg.findNode(forest, "wind")
        theta = glfw.get_time()
        if (0.3*np.cos(theta)>0):
            leavesWindNode.transform = tr.shearing(0.3*np.cos(theta),0,0,0,0,0)
        else:
            leavesWindNode.transform = tr.identity()
        # Drawing the Car
        sg.drawSceneGraphNode(forest, shaderProgram, tr.identity())

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    
    glfw.terminate()