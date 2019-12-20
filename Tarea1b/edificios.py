# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Drawing a car via a scene graph
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import random
import transformations as tr
import scene_graph as sg
import sys

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
INT_BYTES = 4


# A class to store the application control
class Controller:
    x = 0.0
    y = 0.0
    zoom = 1.0
    useNight = False


# A class to make all the buildings using the parameters given
class Buildings:
    def __init__(self, number_of_buildings):
        # number of buildings

        self.number_buildings = number_of_buildings

        # width of all the buildings
        self.w = (2 - 0.2) / number_of_buildings

        # heigth of each building
        self.h_building = []
        for _ in range(0, number_of_buildings):
            self.h_building += [random.randint(1, 10)]

        # color of all the buildings
        self.gpuQuadBuild = \
            createQuad(random.randint(0, 100) / 100.0, random.randint(0, 100) / 100.0, random.randint(0, 100) / 100.0)

        # width of all the windows
        self.w_window = (self.w - self.w / 10) / 10

        # heigth of all the windows
        self.h_window = 0.08
        # random value for the different windows
        self.r = []
        for i in range(0, number_of_buildings):
            self.r += [random.randint(1, 5)]
        # color of a window
        self.gpuQuadWindow = createQuad(0.0, 0.0, 0.0)
        self.gpuQuadWindow2 = createQuad(0.01, 0.01, 0.01)

    def draw_building(self, shader_program, transform_world):

        for i in range(0, self.number_buildings):
            bx = self.get_coord_building(i)
            h = self.h_building[i]
            transform_building = tr.matmul([
                tr.scale(self.w, h / 10, 1.0),
                tr.translate(bx, -(0.5 - (h / 20)), 0.0),
                transform_world
            ])
            drawShape(shader_program, self.gpuQuadBuild, transform_building)

            for j in range(0, h):
                for k in range(0, 10):
                    wx, wy = self.get_coord_windows(k, j)
                    transform_window = tr.matmul([
                        tr.scale(self.w_window, self.h_window, 1.0),
                        tr.translate(wx, wy, 0.0),
                        tr.translate(bx, -(0.49 - self.h_window / 2), 0.0),
                        transform_world
                    ])
                    if ((j + k) % self.r[i]) == 0:
                        drawShape(shaderProgram, self.gpuQuadWindow, transform_window)
                    else:
                        drawShape(shaderProgram, self.gpuQuadWindow2, transform_window)

    def get_coord_building(self, x_building):
        separation_building = 0.2 / (self.number_buildings + 1)
        a = -1 + separation_building + self.w / 2 + (self.w + separation_building) * x_building
        return a

    def get_coord_windows(self, x_window, y_window):
        separation_window_horizontal = self.w / 110
        a = -(self.w / 2) + self.w_window / 2 + separation_window_horizontal + x_window * (
                    self.w_window + separation_window_horizontal)
        b = y_window * (self.h_window + 0.02)
        return a, b


# we will use the global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):
    global controller

    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_LEFT:
            controller.x -= 0.01
        elif key == glfw.KEY_RIGHT:
            controller.x += 0.01
        elif key == glfw.KEY_UP:
            controller.y += 0.01
        elif key == glfw.KEY_DOWN:
            controller.y -= 0.01
        elif key == glfw.KEY_Q:
            controller.zoom -= 0.01
        elif key == glfw.KEY_W:
            controller.zoom += 0.01

    if action != glfw.PRESS:
        return
    elif key == glfw.KEY_SPACE:
        controller.useNight = not controller.useNight

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


# drawshape function allowing for transformations
def drawShape(shaderProgram, shape, transform):
    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # updating the new transform attribute
    glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_FALSE, transform)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)

#basic shapes
def createQuad(r, g, b):
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions        colors
        -0.5, -0.5, 0.0, r, g, b,
        0.5, -0.5, 0.0, r, g, b,
        0.5, 0.5, 0.0, r, g, b,
        -0.5, 0.5, 0.0, r, g, b
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype=np.uint32)

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
        -0.5, 0.0, 0.0, r, g, b,
        0.5, 0.0, 0.0, r, g, b,
        0.0, 0.5, 0.0, r, g, b,
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         ], dtype=np.uint32)

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


def createCircle(r, g, b):
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape

    vertexData = np.array([
        0.0, 0.0, 0.0, r, g, b
    ], dtype=np.float32)
    for i in range(0, 360):
        vertexData = np.concatenate((vertexData,
                                     np.array([0.5 * np.cos(i / (np.pi / 180)), 0.5 * np.sin(i / (np.pi / 180)), 0.0,
                                               r, g, b
                                               ],
                                              dtype=np.float32)))
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array([
        0, 1, 2
    ], dtype=np.uint32)
    for i in range(0, 359):
        indices = np.concatenate((indices, np.array([0, 1 + i, 2 + i], dtype=np.uint32)))
    indices = np.concatenate((indices, np.array([0, 360, 1], dtype=np.uint32)))
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


# modification of createTriangle to allow a degradation in color
def createMountain(r, g, b):
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions        colors
        -0.5, 0.0, 0.0, r, g, b,
        0.5, 0.0, 0.0, r, g, b,
        0.0, 0.5, 0.0, r + 0.3, g + 0.3, b + 0.3,
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         ], dtype=np.uint32)

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

# since snow is a small object, we create a function for itself
def createSnow():
    # Here the new shape will be stored
    gpuShape = sg.GPUShape()

    # Defining locations and colors for each vertex of the shape
    vertexData = np.array([
        #   positions        colors
        -0.5, 0.0, 0.0, 1.0, 1.0, 1.0,
        0.0, 0.5, 0.0, 1.0, 1.0, 1.0,
        0.5, 0.0, 0.0, 1.0, 1.0, 1.0,
        0.25, -0.25, 0.0, 1.0, 1.0, 1.0,
        0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
        -0.25, -0.25, 0.0, 1.0, 1.0, 1.0,
        # It is important to use 32 bits data
    ], dtype=np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 4,
         4, 5, 0
         ], dtype=np.uint32)

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


def create_background():
    # creating the sky
    sky = sg.SceneGraphNode("sky")
    sky.transform = tr.uniformScale(5)
    sky.childs += [createQuad(25 / 255.0, 158 / 255.0, 218 / 255.0)]

    # creating a sun
    sun = sg.SceneGraphNode("sun")
    sun.transform = tr.identity()
    sun.childs += [createCircle(251 / 255.0, 195 / 255.0, 16 / 255.0)]

    # creating the ground
    ground = sg.SceneGraphNode("ground")
    ground.transform = tr.matmul([tr.scale(5, 1, 1), tr.translate(0.0, -1.0, 0.0)])
    ground.childs += [createQuad(158 / 255.0, 219 / 255.0, 26 / 255.0)]

    # creating a couple clouds
    cloud_base = sg.SceneGraphNode("cloud_base")
    cloud_base.transform = tr.matmul([tr.uniformScale(0.2), tr.translate(0.0, 0.8, 0.0)])
    cloud_base.childs += [createCircle(1, 1, 1)]

    cloud_ru = sg.SceneGraphNode("cloud_ru")
    cloud_ru.transform = tr.translate(-0.08, 0.03, 0.0)
    cloud_ru.childs += [cloud_base]

    cloud_rd = sg.SceneGraphNode("cloud_rd")
    cloud_rd.transform = tr.translate(-0.16, -0.03, 0.0)
    cloud_rd.childs += [cloud_base]

    cloud_lu = sg.SceneGraphNode("cloud_lu")
    cloud_lu.transform = tr.translate(0.08, 0.03, 0.0)
    cloud_lu.childs += [cloud_base]

    cloud_ld = sg.SceneGraphNode("cloud_ld")
    cloud_ld.transform = tr.translate(0.16, -0.03, 0.0)
    cloud_ld.childs += [cloud_base]

    cloud_final = sg.SceneGraphNode("cloud_final")
    cloud_final.childs += [cloud_base, cloud_ru, cloud_rd, cloud_ld, cloud_lu]

    cloud_1 = sg.SceneGraphNode("cloud_1")
    cloud_1.transform = tr.translate(-0.5, 0.1, 0.0)
    cloud_1.childs += [cloud_final]

    cloud_2 = sg.SceneGraphNode("cloud_2")
    cloud_2.transform = tr.translate(0.5, -0.1, 0.0)
    cloud_2.childs += [cloud_final]

    # creating a mountain range including snow
    snow = sg.SceneGraphNode("snow")
    snow.transform = tr.matmul([tr.uniformScale(0.5), tr.translate(0.0, 0.25, 0.0)])
    snow.childs += [createSnow()]

    mountain_base = sg.SceneGraphNode("mountain_base")
    mountain_base.transform = tr.matmul([tr.uniformScale(2), tr.translate(0.0, -0.5, 0.0)])
    mountain_base.childs += [createMountain(45 / 255.0, 39 / 255.0, 22 / 255.0)]

    mountain_center = sg.SceneGraphNode("mountain_center")
    mountain_center.childs += [mountain_base]
    mountain_center.childs += [snow]

    mountain_left = sg.SceneGraphNode("mountain_left")
    mountain_left.transform = tr.translate(-0.75, 0.0, 0.0)
    mountain_left.childs += [mountain_base]
    mountain_left.childs += [snow]

    mountain_right = sg.SceneGraphNode("mountain_right")
    mountain_right.transform = tr.translate(0.75, 0.0, 0.0)
    mountain_right.childs += [mountain_base]
    mountain_right.childs += [snow]

    mountain_range = sg.SceneGraphNode("mountain_range")
    mountain_range.childs += [mountain_left, mountain_center, mountain_right]

    # constructing the background
    background = sg.SceneGraphNode("background")
    background.childs += [sky]
    background.childs += [sun]
    background.childs += [mountain_range]
    background.childs += [ground]
    background.childs += [cloud_1]
    background.childs += [cloud_2]
    return background


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
    vertex_shader = """
    #version 130

    uniform mat4 transform;

    in vec3 position;
    in vec3 color;

    out vec3 fragColor;
    void main()
    {
        gl_Position = transform * vec4(position, 1.0f);
        fragColor = color;
    }
    """

    fragment_shader1 = """
   #version 130

   in vec3 fragColor;
   out vec4 outColor;

   void main()
   {
       outColor = vec4(
           fragColor,
           1.0f);
   }
   """

    fragment_shader2 = """
    #version 130

    in vec3 fragColor;
    out vec4 outColor;

    void main()
    {   
        if (fragColor.x+fragColor.y+fragColor.z == 0.03)
        {
        outColor= vec4(1.0,1.0,0.0,1.0f);
        }
        else
        {
        outColor= vec4(
            fragColor.x * 0.2,
            fragColor.y * 0.2,
            clamp(fragColor.z +0.2, 0, 1) * 0.8,
            1.0f);
        }
    }
    """
    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader1, GL_FRAGMENT_SHADER))

    shaderProgram2 = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader2, GL_FRAGMENT_SHADER))

    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Creating shapes on GPU memory
    background = create_background()
    building = Buildings(int(sys.argv[1]))

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    y_sun = 0
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        if controller.useNight:
            glUseProgram(shaderProgram2)
            if y_sun > -0.5:
                y_sun -= 0.1
        else:
            glUseProgram(shaderProgram)
            if y_sun < 1:
                y_sun += 0.1

        sunNode = sg.findNode(background, "sun")
        sunNode.transform = tr.translate(0.0, y_sun, 0.0)

        transform = tr.matmul([
            tr.uniformScale(controller.zoom),
            tr.translate(controller.x, controller.y, 0.0)
        ])

        # Drawing the Car
        sg.drawSceneGraphNode(background, shaderProgram, transform)
        building.draw_building(shaderProgram, transform)
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
