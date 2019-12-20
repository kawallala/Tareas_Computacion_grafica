# imports necessary for use
import glfw
from OpenGL.GL import *
from lib.mathlib import Point3
import sys

# imports from library
import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph2 as sg
import lib.transformations2 as tr2
import lib.camera as cam
import lib.wireframe as wire
import lib.skybox as sky
import lib.interpolations as interpol
import numpy as np

import lib.basic_shapes_extended as bs_ext
import lib.lights as light

_WIREFRAME_ANGLES = list(0 for _ in range(12))

# Setting the default KeyFrames.
_KEYFRAME1_ANGLES = [
    -0.7142656520272039,
    -0.6253455639489346,
    0.39349086634789415,
    -0.3978788737899178,
    -0.34214965115090007,
    -0.22720209469308883,
    0.3623577544766724,
    0.52336595125165,
    -0.49026082134069865,
    -0.15179985849835645,
    0.20612281053395487,
    0.4564325846952399,
]

_KEYFRAME2_ANGLES = [
    -0.30345401401064154,
    -0.6366080031579388,
    -0.06597042046270771,
    -0.07550236802259847,
    -0.872183223851856,
    0.8614180480286306,
    0.35558280910807993,
    0.2988979063646411,
    0.35558280910807993,
    0.003537548135094685,
    0.6851938352637903,
    -0.6693080885036924,
]
# setting our keyframes for interpolation
keyframes = [
    _WIREFRAME_ANGLES,
    _KEYFRAME1_ANGLES,
    _WIREFRAME_ANGLES,
    _KEYFRAME2_ANGLES,
    _WIREFRAME_ANGLES,
]

frames_matrix = list(list(0 for _ in range(12)) for _ in range(17))
frames_matrix[0] = _WIREFRAME_ANGLES
frames_matrix[4] = _KEYFRAME1_ANGLES
frames_matrix[8] = _WIREFRAME_ANGLES
frames_matrix[12] = _KEYFRAME2_ANGLES
frames_matrix[16] = _WIREFRAME_ANGLES

# interpolating keyframes
interpolation_methods = ["linear", "sine", "quadratic"]
interpol.interpolMatrix(0, 4, frames_matrix)
interpol.interpolMatrix(4, 8, frames_matrix)
interpol.interpolMatrix(8, 12, frames_matrix)
interpol.interpolMatrix(12, 16, frames_matrix)


# Controller for program management
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.current_body_part = 0
        self.angle = 0
        self.firstPerson = False
        self.selectedKeyFrame = 0
        self.moving_allowed = True
        self.interpolation_function = 0
        self.texture = True


controller = Controller()

# Create camera for general view
camera = cam.CameraR(r=3)
camera.set_r_vel(0.1)

# Create wireframe
wire = wire.wireframe()

# Create skybox
sky = sky.skybox()

# Create camera for first person view
FirstPersonCamera = cam.CameraXYZ(
    Point3(wire.x_position, wire.y_position, 0.75),
    Point3(wire.x_position, wire.y_position, 0.70),
)

# on_key function for key strokes
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
        elif key == glfw.KEY_P:
            print(_WIREFRAME_ANGLES)

        # in-place movement
        elif key == glfw.KEY_C:
            controller.selectedKeyFrame = (controller.selectedKeyFrame + 1) % (
                len(frames_matrix) - 1
            )
        # toggle for individual movement
        elif key == glfw.KEY_M:
            controller.moving_allowed = not controller.moving_allowed
            if controller.moving_allowed:
                print("movement not allowed")
            else:
                print("movement allowed")

        #change currently moving body part
        elif key == glfw.KEY_R:
            controller.angle = 0
            _WIREFRAME_ANGLES[controller.current_body_part % 12] = controller.angle
            controller.current_body_part = (controller.current_body_part + 1) % 12

        elif key == glfw.KEY_Y:
            controller.angle = 0
            _WIREFRAME_ANGLES[controller.current_body_part % 12] = controller.angle
            controller.current_body_part = (controller.current_body_part - 1) % 12

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

        # Translations of the body
        elif key == glfw.KEY_UP:
            wire.x_position += 0.03 * np.cos(wire.theta)
            wire.y_position += 0.03 * np.sin(wire.theta)
            controller.selectedKeyFrame = (controller.selectedKeyFrame + 1) % (
                len(frames_matrix) - 1
            )
            wire.set_all_angles(frames_matrix[controller.selectedKeyFrame])

        elif key == glfw.KEY_DOWN:
            wire.x_position -= 0.03 * np.cos(wire.theta)
            wire.y_position -= 0.03 * np.sin(wire.theta)
            controller.selectedKeyFrame = (controller.selectedKeyFrame - 1) % (
                len(frames_matrix) - 1
            )
            wire.set_all_angles(frames_matrix[controller.selectedKeyFrame])

        # rotations of the body
        elif key == glfw.KEY_LEFT:
            wire.theta += 0.05

        elif key == glfw.KEY_RIGHT:
            wire.theta -= 0.05

        # changing interpolation method and printing it
        elif key == glfw.KEY_TAB:
            controller.interpolation_function = (
                controller.interpolation_function + 1
            ) % len(interpolation_methods)
            print(interpolation_methods[controller.interpolation_function])
            interpol.interpolMatrix(
                0,
                4,
                frames_matrix,
                interpolation_methods[controller.interpolation_function],
            )

            interpol.interpolMatrix(
                4,
                8,
                frames_matrix,
                interpolation_methods[controller.interpolation_function],
            )

            interpol.interpolMatrix(
                8,
                12,
                frames_matrix,
                interpolation_methods[controller.interpolation_function],
            )

            interpol.interpolMatrix(
                12,
                16,
                frames_matrix,
                interpolation_methods[controller.interpolation_function],
            )

    # print current angles
    if key == glfw.KEY_P:
        wire.print_angles()

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

    # Creating the wireFrame
    obj_wire = wire.create_wireframe(controller.texture)

    # Creating the skybox
    obj_sky = sky.create_skybox(controller.texture)

    # Create shader programs
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()
    texturePipeline = es.SimpleTextureModelViewProjectionShaderProgram()

    if controller.texture:
        glUseProgram(texturePipeline.shaderProgram)
        pipeline = texturePipeline
    else:
        glUseProgram(colorShaderProgram.shaderProgram)
        pipeline = colorShaderProgram
    wire.shader = pipeline

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need t check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Main execution loop
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Create projection
        projection = tr2.perspective(45, float(width) / float(height), 0.1, 100)
        # Setting first person view
        if controller.firstPerson:

            FirstPersonCamera.center_x(np.cos(wire.theta) + wire.x_position)
            FirstPersonCamera.center_y(np.sin(wire.theta) + wire.y_position)
            view = FirstPersonCamera.get_view()
            FirstPersonCamera.set_x(wire.x_position)
            FirstPersonCamera.set_y(wire.y_position)

        else:
            # Get camera view matrix
            view = camera.get_view()

        glUniformMatrix4fv(
            glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view
        )
        glUniformMatrix4fv(
            glGetUniformLocation(pipeline.shaderProgram, "projection"),
            1,
            GL_TRUE,
            projection,
        )

        angle = np.cos(controller.angle)

        if controller.moving_allowed:
            # Moving with KeyFrames.
            wire.set_all_angles(frames_matrix[controller.selectedKeyFrame])
        else:
            wire.set_bodypart_angle(controller.current_body_part, angle)
        # Drawing objects
        sg.drawSceneGraphNode(obj_wire, pipeline)
        sg.drawSceneGraphNode(obj_sky, pipeline)
        # rotating and moving the human
        wire.rotate_human()
        wire.move_human()
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen
        glfw.swap_buffers(window)
    glfw.terminate()
