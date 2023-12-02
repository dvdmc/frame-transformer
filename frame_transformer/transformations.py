"""
    Code for the functions to transform a pose from one frame to another.
"""
from dataclasses import dataclass
from typing import Literal, Tuple
import numpy as np
import quaternion

from frame_transformer.frames import Frame


@dataclass
class AxisMapping:
    """
    This class maps an axis to another axis.
    It is used to map the axis of a frame to another frame.
    """

    f_from_to: Tuple[int, int]
    h_from_to: Tuple[int, int]
    v_from_to: Tuple[int, int]

    h_inverted: bool
    v_inverted: bool

    def __str__(self):
        output = ""
        output += f"Forward: {self.f_from_to[0]} -> {self.f_from_to[1]}\n"
        output += f"Horizontal: {self.h_from_to[0]} -> {self.h_from_to[1]}\n"
        output += f"Vertical: {self.v_from_to[0]} -> {self.v_from_to[1]}\n"
        output += f"Horizontal inverted: {self.h_inverted}\n"
        output += f"Vertical inverted: {self.v_inverted}\n"

        return output

AXIS_DICT = {
    "x": 0,
    "y": 1,
    "z": 2,
}

STRING_AXIS_DICT = {
    0: "x",
    1: "y",
    2: "z",
}

def _find_mapping(initial: Frame, target: Frame) -> AxisMapping:
    """
    This function finds the mapping from one frame to another.
    It does not check for the handedness of the frames.
    """
    # We find the mapping from initial to target
    forward_init = AXIS_DICT[initial[0]]
    h_init = AXIS_DICT[initial[2]]
    h_dir_init = initial[3]
    v_init = AXIS_DICT[initial[5]]
    v_dir_init = initial[6]

    forward_target = AXIS_DICT[target[0]]
    h_target = AXIS_DICT[target[2]]
    h_dir_target = target[3]
    v_target = AXIS_DICT[target[5]]
    v_dir_target = target[6]

    is_inverted_h = h_dir_init != h_dir_target
    is_inverted_v = v_dir_init != v_dir_target

    return AxisMapping(
        f_from_to=(forward_init, forward_target),
        h_from_to=(h_init, h_target),
        v_from_to=(v_init, v_target),
        h_inverted=is_inverted_h,
        v_inverted=is_inverted_v,
    )


def _translation_change(t: np.ndarray, initial: Frame, target: Frame) -> np.ndarray:
    """
    This function changes the translation vector from one frame to another.
    It finds the mapping from initial to target axis and applies it.
    If the axis are inverted, it inverts the translation vector.
    It does not check for the handedness of the frames.
    """
    # We find the mapping from initial to target
    axis_mapping = _find_mapping(initial, target)

    # We apply the mapping
    new_t = np.zeros(3)
    # Forward
    new_t[axis_mapping.f_from_to[1]] = t[axis_mapping.f_from_to[0]]
    # Horizontal
    new_t[axis_mapping.h_from_to[1]] = t[axis_mapping.h_from_to[0]]
    # Vertical
    new_t[axis_mapping.v_from_to[1]] = t[axis_mapping.v_from_to[0]]

    # We invert the axis if needed
    # Horizontal
    if axis_mapping.h_inverted:
        new_t[axis_mapping.h_from_to[1]] = -t[axis_mapping.h_from_to[0]]
    # Vertical
    if axis_mapping.v_inverted:
        new_t[axis_mapping.v_from_to[1]] = -t[axis_mapping.v_from_to[0]]

    return new_t


def _rotation_change_rot_matrix(R: np.ndarray, initial: Frame, target: Frame) -> np.ndarray:
    """
    This function changes the rotation matrix (3x3) from one frame to another.
    """
    # We find the mapping from initial to target
    axis_mapping = _find_mapping(initial, target)
    # We apply the mapping. Modify the rotation matrix
    rot = np.zeros((3, 3))
    # Forward
    rot[axis_mapping.f_from_to[1], axis_mapping.f_from_to[0]] = 1
    # Horizontal
    rot[axis_mapping.h_from_to[1], axis_mapping.h_from_to[0]] = 1
    # Vertical
    rot[axis_mapping.v_from_to[1], axis_mapping.v_from_to[0]] = 1
    # We invert the axis if needed
    # Horizontal
    if axis_mapping.h_inverted:
        rot[axis_mapping.h_from_to[1], axis_mapping.h_from_to[0]] = -1
    # Vertical
    if axis_mapping.v_inverted:
        rot[axis_mapping.v_from_to[1], axis_mapping.v_from_to[0]] = -1

    return rot @ R

def _get_rotation_matrix(initial: Frame, target: Frame) -> np.ndarray:
    """
        This function returns the rotation matrix for the frame transformation.
    """
    # We find the mapping from initial to target
    axis_mapping = _find_mapping(initial, target)
    # We apply the mapping. Modify the rotation matrix
    rot = np.zeros((3, 3))
    # Forward
    rot[axis_mapping.f_from_to[1], axis_mapping.f_from_to[0]] = 1
    # Horizontal
    rot[axis_mapping.h_from_to[1], axis_mapping.h_from_to[0]] = 1
    # Vertical
    rot[axis_mapping.v_from_to[1], axis_mapping.v_from_to[0]] = 1
    # We invert the axis if needed
    # Horizontal
    if axis_mapping.h_inverted:
        rot[axis_mapping.h_from_to[1], axis_mapping.h_from_to[0]] = -1
    # Vertical
    if axis_mapping.v_inverted:
        rot[axis_mapping.v_from_to[1], axis_mapping.v_from_to[0]] = -1

    return rot

def _rotation_change_quaternion(q: np.ndarray, initial: Frame, target: Frame) -> np.ndarray:
    """
        This function changes the quaternion from one frame to another.
    """
    rotation_matrix = quaternion.as_rotation_matrix(q)
    new_rotation_matrix = _rotation_change_rot_matrix(rotation_matrix, initial, target)
    new_q = quaternion.from_rotation_matrix(new_rotation_matrix)

    # Transform to numpy array
    new_q = quaternion.as_float_array(new_q)

    return new_q

def _transform(translation: np.ndarray, rotation: np.ndarray, initial: Frame, target: Frame) -> Tuple[np.ndarray, np.ndarray]:
    """
    This function transforms a pose from one frame to another.

    Args:
        translation: The translation vector of the pose in the origin frame.
        rotation: The rotation matrix (3x3) or quaternion (4x1) of the pose in the origin frame.

    Returns:
        The translation vector and rotation matrix or quaternion of the pose in the destination frame.
    """
    # We change the translation vector
    new_t = _translation_change(translation, initial, target)

    # Check if the rotation is a quaternion or a rotation matrix
    if rotation.shape == (4,):
        new_rot = _rotation_change_quaternion(rotation, initial, target)
    else:
        new_rot = _rotation_change_rot_matrix(rotation, initial, target)

    return (new_t, new_rot)
