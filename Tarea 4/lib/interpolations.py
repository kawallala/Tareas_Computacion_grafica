# coding=utf-8
"""
Interpolation Module.
@authors: Martin Araya & Alonso Utreras
"""

import numpy as np
import lib.catrom as cr

"""
Idea: Could do an interpolation for GPUshapes.
def interpolGPUshapes(GPUState1, GPUState2,intermediate_frames, function_type="linear"):
"""


def interpolMatrix(keyframe1, keyframe2, matrix, function_type="linear"):
    """
    Given a interpolation function, it interpolates the angles between two keyframes,
    modifying the columns between the keyframes. In the given matrix, each column is a frame
    """
    assert isinstance(keyframe2, int) and isinstance(keyframe1, int)
    if keyframe2 > keyframe1:

        first_frame = matrix[keyframe1]
        last_frame = matrix[keyframe2]
        difference = keyframe2 - keyframe1
        # we are gonna need the difference between keyframe 2 and keyframe 1, so we can
        # divide it in equal steps

        if function_type == "linear":
            delta_t = 1 / difference
            t = delta_t
            for column in range(keyframe1 + 1, keyframe2, 1):
                # for each frame representing  column
                frame = matrix[column]
                for angle in range(12):  # for each angle (representing a row in a column)
                    frame[angle] = first_frame[angle] * (1 - t) + last_frame[angle] * t
                t += delta_t

        elif function_type == "sine":
            delta_t = np.pi / 2 / difference
            t = delta_t
            # for t in range(0, np.pi / 2, total_frames + 1)
            for column in range(keyframe1 + 1, keyframe2, 1):
                # for each frame representing  column
                frame = matrix[column]
                for angle in range(12):
                    frame[angle] = first_frame[angle] * (1 - np.sin(t)) + last_frame[angle] * np.sin(t)
                t += delta_t

        elif function_type == "quadratic":
            delta_t = 1 / difference
            t = delta_t
            for column in range(keyframe1 + 1, keyframe2, 1):
                # for each frame representing  column
                frame = matrix[column]
                for angle in range(12):  # for each angle (representing a row in a column)
                    frame[angle] = first_frame[angle] * (1 - t)*(1-t) + last_frame[angle] * t * t
                t += delta_t


# if function_type == "sine":
    #    first_frame = matrix[keyframe1]
     #   last_frame = matrix[keyframe2]
      #  difference = keyframe2 - keyframe1
       #



def interpolArrayAngles(keyframe1, keyframe2, total_frames=3, function_type="linear"):
    assert len(keyframe1) == len(keyframe2)
    generated_frames = []
    generated_frames.append(keyframe1)  # begin state
    # generated_frames[-1] = keyframe2  # final state
    ans = list(0 for _ in range(len(keyframe1)))  # ans is a list of len equals to keyframe1's len

    t_i = np.linspace(0, 1, num=total_frames, endpoint=True)  # doing linear interpolation
    if function_type == "linear":
        for frame in range(1, total_frames):  # for every intermediate_frame
            for i in range(len(keyframe1)):  # for each angle
                ans[i] = keyframe1[i] * (1 - t_i[frame]) + keyframe2[i] * t_i[frame]
            generated_frames.append(ans.copy())

        return generated_frames

    elif function_type == "sine":
        for i in range(len(keyframe1)):  # for each angle
            for t in range(0, np.pi / 2, total_frames + 1):  # interpolating with angles
                ans[i] = keyframe1[i] * (1 - np.sin(t)) + keyframe2[i] * np.sin(t)
        return ans

    else:
        raise Exception("No valid function given.")


def interpol_keyframes_wireframe(keyframe1, keyframe2, wireframe, total_frames=3, function_type="linear"):
    assert len(keyframe1) == len(keyframe2)
    generated_frames = []
    generated_frames.append(keyframe1)  # begin state
    # generated_frames[-1] = keyframe2  # final state
    ans = list(0 for _ in range(len(keyframe1)))  # ans is a list of len equals to keyframe1's len

    t_i = np.linspace(0, 1, num=total_frames, endpoint=True)  # doing linear interpolation
    if function_type == "linear":
        for frame in range(1, total_frames):  # for every intermediate_frame
            for i in range(len(keyframe1)):  # for each angle
                ans[i] = keyframe1[i] * (1 - t_i[frame]) + keyframe2[i] * t_i[frame]
            generated_frames.append(ans.copy())

        return generated_frames

    elif function_type == "sine":
        for i in range(len(keyframe1)):  # for each angle
            for t in range(0, np.pi / 2, total_frames + 1):  # interpolating with angles
                ans[i] = keyframe1[i] * (1 - t) + keyframe2[i] * t
        return ans

    else:
        raise Exception("No valid function given.")
