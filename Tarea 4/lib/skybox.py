import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph2 as sg
import lib.transformations2 as tr2
import numpy as np
from OpenGL.GL import *

# Constants


class skybox:
    """
    Skybox for the character to move in
    """

    def __init__(self):
        """
        constructor
        """

    def create_skybox(self, texture):
        # basics shapes used
        if texture:
            gpu_cube_grass = es.toGPUShape(
                bs.createTextureQuad("grass3.jpg"), GL_REPEAT, GL_LINEAR
            )
            gpu_cube_sky = es.toGPUShape(
                bs.createTextureQuad("sky_2.jpg"), GL_REPEAT, GL_LINEAR
            )
        else:
            gpu_cube_grass = es.toGPUShape(bs.createColorQuad(1, 1, 1))
            gpu_cube_sky = es.toGPUShape(bs.createColorQuad(0, 0, 1))

        floor = sg.SceneGraphNode("floor")
        floor.transform = tr2.matmul([tr2.uniformScale(10)])
        floor.childs += [gpu_cube_grass]

        wall_1 = sg.SceneGraphNode("wall_1")
        wall_1.transform = tr2.matmul(
            [tr2.translate(0, 5, 2.5), tr2.rotationX(np.pi / 2), tr2.scale(10, 5, 10)]
        )
        wall_1.childs += [gpu_cube_sky]

        wall_2 = sg.SceneGraphNode("wall_2")
        wall_2.transform = tr2.rotationZ(np.pi / 2)
        wall_2.childs += [wall_1]

        wall_3 = sg.SceneGraphNode("wall_3")
        wall_3.transform = tr2.rotationZ(np.pi / 2)
        wall_3.childs += [wall_2]

        wall_4 = sg.SceneGraphNode("wall_4")
        wall_4.transform = tr2.rotationZ(np.pi / 2)
        wall_4.childs += [wall_3]

        wall_top = sg.SceneGraphNode("wall_top")
        wall_top.transform = tr2.translate(0, 0, 5)
        wall_top.childs += [floor]

        skybox = sg.SceneGraphNode("skybox")
        skybox.childs += [floor, wall_1, wall_2, wall_3, wall_4, wall_top]

        return skybox
