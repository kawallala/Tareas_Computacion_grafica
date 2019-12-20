import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.scene_graph2 as sg
import lib.transformations2 as tr2
import numpy as np
from OpenGL.GL import *

# Constants
_WIREFRAME_ANGLES = list(0 for _ in range(12))
_BODY_PARTS = [
    "left_hand_rotation",  # "Left hand",
    "lower_left_rotation_arm",  # "Left lower arm",
    "left_rotation_arm",  # "Left arm",
    "right_hand_rotation",  # "Right hand",
    "lower_right_arm_rotation",  # "Right lower arm",
    "right_arm_rotation",  # "Right arm",
    "left_feet_rotation",  # "Left feet",
    "lower_left_leg_rotation",  # "Left lower leg",
    "left_leg_rotation",  # "Left leg",
    "right_feet_rotation",  # "Right feet",
    "lower_right_leg_rotation",  # Right lower leg
    "right_leg_rotation",  # Right leg
]


class wireframe:
    """
    class for the wireframe to be used
    """

    def __init__(self):
        """
        constructor
        """
        self.angles = _WIREFRAME_ANGLES
        self.mainNode = sg.SceneGraphNode("Null")  # Before creation of wireFrame
        self.x_position = 0
        self.y_position = 0
        self.theta = 0
        self.moved = False
        self.shader = None

    def create_wireframe(self, texture):
        # Basic shapes used
        if texture:
            gpu_cube_head = es.toGPUShape(
                bs.createTextureCube("steve_head.png"), GL_REPEAT, GL_LINEAR
            )
            gpu_cube_hair = es.toGPUShape(
                bs.createTextureCube("hair.jpg"), GL_REPEAT, GL_LINEAR
            )
            gpu_cube_torso = es.toGPUShape(
                bs.createTextureCube("shirt.jpg"), GL_REPEAT, GL_LINEAR
            )
            gpu_cube_arm_upper = es.toGPUShape(
                bs.createTextureCube("shirt.jpg"), GL_REPEAT, GL_LINEAR
            )
            gpu_cube_arm_lower = es.toGPUShape(
                bs.createTextureCube("skin2.jpg"), GL_REPEAT, GL_LINEAR
            )
            gpu_cube_hand = es.toGPUShape(
                bs.createTextureCube("skin2.jpg"), GL_REPEAT, GL_LINEAR
            )
        else:
            gpu_cube_head = es.toGPUShape(bs.createColorCube(1, 1, 1))
            gpu_cube_hair = es.toGPUShape(bs.createColorCube(1, 1, 0))
            gpu_cube_torso = es.toGPUShape(bs.createColorCube(1, 1, 1))
            gpu_cube_arm_upper = es.toGPUShape(bs.createColorCube(0, 1, 0))
            gpu_cube_arm_lower = es.toGPUShape(bs.createColorCube(0, 0, 1))
            gpu_cube_hand = es.toGPUShape(bs.createColorCube(1, 0, 0))

        # generic nodes
        head = sg.SceneGraphNode("head")
        head.transform = tr2.matmul([tr2.translate(0, 0, 0.675), tr2.uniformScale(0.1)])
        head.childs += [gpu_cube_head]

        hair = sg.SceneGraphNode("hair")
        hair.transform = tr2.matmul(
            [tr2.translate(-0.0006, 0, 0.69), tr2.uniformScale(0.101)]
        )
        hair.childs += [gpu_cube_hair]

        torso = sg.SceneGraphNode("torso")
        torso.transform = tr2.matmul(
            [tr2.translate(0, 0, 0.475), tr2.scale(0.1, 0.2, 0.3)]
        )
        torso.childs += [gpu_cube_torso]

        hand = sg.SceneGraphNode("hand")
        hand.transform = tr2.matmul(
            [tr2.translate(0, 0, -0.025), tr2.uniformScale(0.05)]
        )
        hand.childs += [gpu_cube_hand]

        lower_arm = sg.SceneGraphNode("lower_arm")
        lower_arm.transform = tr2.matmul(
            [tr2.translate(0, 0, -0.05), tr2.scale(0.05, 0.05, 0.1)]
        )
        lower_arm.childs += [gpu_cube_arm_lower]

        upper_arm = sg.SceneGraphNode("upper_arm")
        upper_arm.transform = tr2.matmul(
            [tr2.translate(0, 0, -0.05), tr2.scale(0.05, 0.05, 0.1)]
        )
        upper_arm.childs += [gpu_cube_arm_upper]

        feet = sg.SceneGraphNode("feet")
        feet.transform = tr2.matmul(
            [tr2.translate(0.025, 0, -0.025), tr2.scale(0.1, 0.05, 0.05)]
        )
        feet.childs += [gpu_cube_hand]

        lower_leg = sg.SceneGraphNode("lower_leg")
        lower_leg.transform = tr2.matmul(
            [tr2.translate(0, 0, -0.0625), tr2.scale(0.05, 0.05, 0.125)]
        )
        lower_leg.childs += [gpu_cube_arm_lower]

        upper_leg = sg.SceneGraphNode("upper_leg")
        upper_leg.transform = tr2.matmul(
            [tr2.translate(0, 0, -0.075), tr2.scale(0.05, 0.05, 0.15)]
        )
        upper_leg.childs += [gpu_cube_arm_upper]

        ######################################################################
        # construction of mobile structures

        # Left arm
        left_hand_rotation = sg.SceneGraphNode("left_hand_rotation")
        left_hand_rotation.transform = tr2.rotationY(self.angles[0])
        left_hand_rotation.childs += [hand]

        left_hand_translation = sg.SceneGraphNode("left_hand_translation")
        left_hand_translation.transform = tr2.translate(0, 0, -0.1)
        left_hand_translation.childs += [left_hand_rotation]

        lower_left_rotation_arm = sg.SceneGraphNode("lower_left_rotation_arm")
        lower_left_rotation_arm.transform = tr2.rotationY(self.angles[1])
        lower_left_rotation_arm.childs += [lower_arm, left_hand_translation]

        lower_left_arm_translation = sg.SceneGraphNode("lower_left_arm_translation")
        lower_left_arm_translation.transform = tr2.translate(0, 0, -0.1)
        lower_left_arm_translation.childs += [lower_left_rotation_arm]

        left_arm_rotation = sg.SceneGraphNode("left_rotation_arm")
        left_arm_rotation.transform = tr2.rotationY(self.angles[2])
        left_arm_rotation.childs += [upper_arm, lower_left_arm_translation]

        left_arm_translation = sg.SceneGraphNode("left_translation_arm")
        left_arm_translation.transform = tr2.translate(0, 0.125, 0.625)
        left_arm_translation.childs += [left_arm_rotation]

        # Right arm
        right_hand_rotation = sg.SceneGraphNode("right_hand_rotation")
        right_hand_rotation.transform = tr2.rotationY(self.angles[3])
        right_hand_rotation.childs += [hand]

        right_hand_translation = sg.SceneGraphNode("right_hand_translation")
        right_hand_translation.transform = tr2.translate(0, 0, -0.1)
        right_hand_translation.childs += [right_hand_rotation]

        lower_right_arm_rotation = sg.SceneGraphNode("lower_right_arm_rotation")
        lower_right_arm_rotation.transform = tr2.rotationY(self.angles[4])
        lower_right_arm_rotation.childs += [lower_arm, right_hand_translation]

        lower_right_arm_translation = sg.SceneGraphNode("lower_right_arm_translation")
        lower_right_arm_translation.transform = tr2.translate(0, 0, -0.1)
        lower_right_arm_translation.childs += [lower_right_arm_rotation]

        right_arm_rotation = sg.SceneGraphNode("right_arm_rotation")
        right_arm_rotation.transform = tr2.rotationY(self.angles[5])
        right_arm_rotation.childs += [upper_arm, lower_right_arm_translation]

        right_arm_translation = sg.SceneGraphNode("right_arm_translation")
        right_arm_translation.transform = tr2.translate(0, -0.125, 0.625)
        right_arm_translation.childs += [right_arm_rotation]

        # Left leg
        left_feet_rotation = sg.SceneGraphNode("left_feet_rotation")
        left_feet_rotation.transform = tr2.rotationY(self.angles[6])
        left_feet_rotation.childs += [feet]

        left_feet_translation = sg.SceneGraphNode("left_feet_translation")
        left_feet_translation.transform = tr2.translate(0, 0, -0.125)
        left_feet_translation.childs += [left_feet_rotation]

        lower_left_leg_rotation = sg.SceneGraphNode("lower_left_leg_rotation")
        lower_left_leg_rotation.transform = tr2.rotationY(self.angles[7])
        lower_left_leg_rotation.childs += [lower_leg, left_feet_translation]

        lower_left_leg_translation = sg.SceneGraphNode("lower_left_leg_translation")
        lower_left_leg_translation.transform = tr2.translate(0, 0, -0.15)
        lower_left_leg_translation.childs += [lower_left_leg_rotation]

        left_leg_rotation = sg.SceneGraphNode("left_leg_rotation")
        left_leg_rotation.transform = tr2.rotationY(self.angles[8])
        left_leg_rotation.childs += [upper_leg, lower_left_leg_translation]

        left_leg_translation = sg.SceneGraphNode("left_leg_translation")
        left_leg_translation.transform = tr2.translate(0, 0.075, 0.325)
        left_leg_translation.childs += [left_leg_rotation]

        # Right leg
        right_feet_rotation = sg.SceneGraphNode("right_feet_rotation")
        right_feet_rotation.transform = tr2.rotationY(self.angles[9])
        right_feet_rotation.childs += [feet]

        right_feet_translation = sg.SceneGraphNode("right_feet_translation")
        right_feet_translation.transform = tr2.translate(0, 0, -0.125)
        right_feet_translation.childs += [right_feet_rotation]

        lower_right_leg_rotation = sg.SceneGraphNode("lower_right_leg_rotation")
        lower_right_leg_rotation.transform = tr2.rotationY(self.angles[10])
        lower_right_leg_rotation.childs += [lower_leg, right_feet_translation]

        lower_right_leg_translation = sg.SceneGraphNode("lower_right_leg_translation")
        lower_right_leg_translation.transform = tr2.translate(0, 0, -0.15)
        lower_right_leg_translation.childs += [lower_right_leg_rotation]

        right_leg_rotation = sg.SceneGraphNode("right_leg_rotation")
        right_leg_rotation.transform = tr2.rotationY(self.angles[11])
        right_leg_rotation.childs += [upper_leg, lower_right_leg_translation]

        right_leg_translation = sg.SceneGraphNode("right_leg_translation")
        right_leg_translation.transform = tr2.translate(0, -0.075, 0.325)
        right_leg_translation.childs += [right_leg_rotation]

        human_rotation = sg.SceneGraphNode("human_rotation")
        human_rotation.childs += [
            left_leg_translation,
            right_leg_translation,
            torso,
            left_arm_translation,
            right_arm_translation,
            head,
            hair,
        ]

        human_translation = sg.SceneGraphNode("human_translation")
        human_translation.childs += [human_rotation]

        self.mainNode = human_translation
        return self.mainNode

    def move_bodyPart_angle(self, bodypart, angle):
        """
        This function finds the node corresponding to the body-part-rotation and sets the angle of it
        :param integer bodypart: the body part. Numbers are correlated to their _BODY_PARTS indexes
        :param angle: the angle to rotate to given written in radians.
        """
        if isinstance(bodypart, int):
            bodypart = (
                bodypart % 12
            )  # Setting a valid bodyPart. This might be unnecessary if done before.
            if isinstance(angle, float) or isinstance(angle, int):
                bodypartname = _BODY_PARTS[
                    bodypart
                ]  # Controlling that the angle is valid for the limb.
                self.angles[bodypart] = min(
                    max(self.angles[bodypart] + angle, -np.pi / 2), np.pi / 2
                )
                body_part_node = sg.findNode(self.mainNode, bodypartname)
                body_part_node.transform = tr2.rotationY(self.angles[bodypart])
            else:
                raise Exception("angle must be int or float")
        else:
            raise Exception("bodypart must be an integer")

    def set_bodypart_angle(self, bodypart, angle):
        """
        sets an angle for a specific body part
        """
        if isinstance(bodypart, int):
            bodypart = (
                bodypart % 12
            )  # Setting a valid bodyPart. This might be unnecessary if done before.
            if isinstance(angle, float) or isinstance(angle, int):

                bodypartname = _BODY_PARTS[
                    bodypart
                ]  # Controlling that the angle is valid for the limb.
                self.angles[bodypart] = angle
                body_part_node = sg.findNode(self.mainNode, bodypartname)
                body_part_node.transform = tr2.rotationY(self.angles[bodypart])

            else:
                raise Exception("angle must be int or float")
        else:
            raise Exception("bodypart must be an integer")

    def set_body_keyframe(self, keyframe):
        """
        sets angles for every body part given the keyframe with a list of angles
        """
        if isinstance(keyframe, list):
            if len(keyframe) == 12:
                self.angles = keyframe
                for bodypart in range(12):
                    bodypartname = _BODY_PARTS[
                        bodypart
                    ]  # Controlling that the angle is valid for the limb.
                    body_part_node = sg.findNode(self.mainNode, bodypartname)
                    body_part_node.transform = tr2.rotationY(self.angles[bodypart])
            else:
                raise Exception("there must be 12 angles given")
        else:
            raise Exception("anglelist must be a list")

    def set_all_angles(self, anglelist):
        """
        sets current angles to a list
        """
        if isinstance(anglelist, list):
            if len(anglelist) == 12:
                self.angles = anglelist
                for bodypart in range(12):
                    bodypartname = _BODY_PARTS[
                        bodypart
                    ]  # Controlling that the angle is valid for the limb.
                    body_part_node = sg.findNode(self.mainNode, bodypartname)
                    body_part_node.transform = tr2.rotationY(self.angles[bodypart])

            else:
                raise Exception("there must be 12 angles given")
        else:
            raise Exception("angle list must be a list")

    def move_human(self):
        """
        Moves the whole body with a translation
        """
        self.mainNode.transform = tr2.translate(self.x_position, self.y_position, 0)

    def draw_human(self):
        sg.drawSceneGraphNode(self.mainNode, self.shader)

    def rotate_human(self):
        """
        Moves the whole body with a translation
        """
        self.mainNode.childs[0].transform = tr2.rotationZ(self.theta)

    def get_angles(self):
        """
        returns a list with all the current angles
        """
        return self.angles

    def print_angles(self):
        """
        prints current angles in the console
        """
        for i in range(12):
            print(_BODY_PARTS[i], ":", self.angles[i])

