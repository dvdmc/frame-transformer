"""
    Code to explain the transformations.
"""
import numpy as np
import quaternion
from scipy.spatial.transform import Rotation as R

from rich.console import Console
from rich import emoji

from frame_transformer.frames import Frame, HAND_DICT
from frame_transformer.systems import System
from frame_transformer.transformations import (
    _find_mapping,
    _get_rotation_matrix,
    STRING_AXIS_DICT,
)

console = Console()

COLOR_DICT = {
    "x": "red",
    "y": "green",
    "z": "blue",
}

COLOR_DICT_NUM = {
    0: "red",
    1: "green",
    2: "blue",
}

H_DICT = {
    "l": "left",
    "r": "right",
}

H_DICT_TO_NEGATED = {
    "l": "",
    "r": "-",
}

V_DICT = {
    "u": "up",
    "d": "down",
}

V_DICT_TO_NEGATED = {
    "u": "",
    "d": "-",
}

EMOJI_DICT = {
    "l": ":backhand_index_pointing_left:",
    "r": ":backhand_index_pointing_right:",
    "rh": ":raised_hand:",
    "lh": ":raised_back_of_hand:",
    "u": ":backhand_index_pointing_up:",
    "d": ":backhand_index_pointing_up:",
    "ok": ":ok_hand:",
}

SYSTEM_EMOJI_DICT = {
    "ros": ":robot_face:",
    "opencv": ":camera:",
    "airsim": ":airplane:",
    "unreal": ":video_game:",
}


def _frame_to_readable(frame: Frame) -> None:
    """
    This function transforms a frame to a readable format.

    Args:
        frame (Frame): The frame to transform.

    Returns:
        str: The readable format.
    """
    forward, horizontal, vertical = frame.split("_")
    horizontal_direction = H_DICT[horizontal[1]]
    horizontal = horizontal[0]
    vertical_direction = V_DICT[vertical[1]]
    vertical = vertical[0]

    return f"[{COLOR_DICT[forward]}]{forward} forward[/], [{COLOR_DICT[horizontal]}]{horizontal_direction}[/] [{COLOR_DICT[horizontal]}]{horizontal}[/] [{COLOR_DICT[vertical]}]{vertical_direction}[/] [{COLOR_DICT[vertical]}]{vertical}[/]"


def _frame_to_vector(frame: Frame) -> str:
    """
    This function transforms a frame to a vector string.

    Args:
        frame (Frame): The frame to transform.

    Returns:
        str: The vector string.
    """
    forward, horizontal, vertical = frame.split("_")
    horizontal_direction = H_DICT_TO_NEGATED[horizontal[1]]
    horizontal = horizontal[0]
    vertical_direction = V_DICT_TO_NEGATED[vertical[1]]
    vertical = vertical[0]

    return (
        f"{forward} {horizontal_direction}{horizontal} {vertical_direction}{vertical}"
    )

def _explain_mapping(origin: Frame, target: Frame) -> None:
    """
    This function explains the mapping between two frames in terms of axes.

    Args:
        origin (Frame): The origin frame.
        target (Frame): The target frame.
    """
    axis_mapping = _find_mapping(origin, target)
    color1 = COLOR_DICT_NUM[axis_mapping.f_from_to[0]]
    axis1 = STRING_AXIS_DICT[axis_mapping.f_from_to[0]]
    color2 = COLOR_DICT_NUM[axis_mapping.f_from_to[1]]
    axis2 = STRING_AXIS_DICT[axis_mapping.f_from_to[1]]
    console.print(
        f"[{color1}]{axis1}[/] :arrow_forward: [{color2}]{axis2}[/].",
    )
    color1 = COLOR_DICT_NUM[axis_mapping.h_from_to[0]]
    axis1 = STRING_AXIS_DICT[axis_mapping.h_from_to[0]]
    color2 = COLOR_DICT_NUM[axis_mapping.h_from_to[1]]
    axis2 = STRING_AXIS_DICT[axis_mapping.h_from_to[1]]
    
    text_inverted = ""
    if axis_mapping.h_inverted:
        text_inverted = "-"
    console.print(
        f"[{color1}]{axis1}[/] :arrow_forward: [yellow]{text_inverted}[/][{color2}]{axis2}[/].",
    )

    color1 = COLOR_DICT_NUM[axis_mapping.v_from_to[0]]
    axis1 = STRING_AXIS_DICT[axis_mapping.v_from_to[0]]
    color2 = COLOR_DICT_NUM[axis_mapping.v_from_to[1]]
    axis2 = STRING_AXIS_DICT[axis_mapping.v_from_to[1]]

    text_inverted = ""
    if axis_mapping.v_inverted:
        text_inverted = "-"
    console.print(
        f"[{color1}]{axis1}[/] :arrow_forward: [yellow]{text_inverted}[/][{color2}]{axis2}[/].",
    )


def _explain_transformation(origin: Frame, target: Frame) -> None:
    """
    This function explains the transformation between two frames.

    Args:
        origin (Frame): The origin frame.
        target (Frame): The target frame.
    """
    vector_origin = _frame_to_vector(origin)
    vector_target = _frame_to_vector(target)

    console.print(
        f"A translation vector with respect to canonical coordinates is: {vector_origin}."
    )
    console.print(f"We want to transform it to {vector_target}.")
    _explain_mapping(origin, target)
    console.rule()
    console.print(
        "A orientation matrix with respect to canonical coordinates is: \n"
        + "[\[r00, r01, r02],\n \[r10, r11, r12],\n \[r20, r21, r22]]"
    )
    rot = _get_rotation_matrix(origin, target)
    console.print(f"The change will compose it with:\n{rot}")
    quat = quaternion.from_rotation_matrix(rot)
    console.print(
        f"This corresponds to the quaternion: {quaternion.as_float_array(quat)} or {quaternion.as_float_array(-quat)}."
    )
    axis_angle = quaternion.as_rotation_vector(quat)
    angle = np.linalg.norm(axis_angle)
    axis = axis_angle / angle
    console.print(f"And to the axis-angle rotation: {np.round(np.rad2deg(angle),2)} degrees around {axis}.")
    euler_xyz = R.from_matrix(rot).as_euler("xyz")
    console.print(
        f"Which is the same as the Euler XYZ angles: {np.rad2deg(euler_xyz)}."
    )
    console.print(f"Done! :+1: :partying_face: :tada: :rocket: :sunglasses: :100:")


def _explain_system(origin: System, target: System) -> None:
    """
    This function explains the transformation between two systems.

    Args:
        origin (System): The origin system.
        target (System): The target system.
    """
    console.print(
        f"You want to transform:\n {SYSTEM_EMOJI_DICT[origin]} {origin} :arrow_forward: {target} {SYSTEM_EMOJI_DICT[target]} :sunglasses:"
    )

def _explain(origin: Frame, target: Frame) -> None:
    """
    This function explains the transformation between two frames.

    Args:
        origin (Frame): The origin frame.
        target (Frame): The target frame.
    """
    readable_origin = _frame_to_readable(origin)
    readable_target = _frame_to_readable(target)
    console.print(
        f"Change:\n{readable_origin} :arrow_forward: {readable_target} :+1:"
    )
    hand_origin = HAND_DICT[origin] + "h"
    hand_target = HAND_DICT[target] + "h"
    console.rule()
    console.print(
        f"{readable_origin} ({H_DICT[HAND_DICT[origin]]}-handed) {EMOJI_DICT[hand_origin]}"
    )
    console.print(
        f"{readable_target} ({H_DICT[HAND_DICT[target]]}-handed) {EMOJI_DICT[hand_target]}"
    )
    do_swap = "not "
    do_same = ""
    if HAND_DICT[origin] != HAND_DICT[target]:
        do_swap = ""
        do_same = "not"

    console.print(
        f"Since the frames are [red]{do_same}[/]the same-handed, we do {do_swap}need to swap the axes."
    )
    console.rule()
    _explain_transformation(origin, target)
