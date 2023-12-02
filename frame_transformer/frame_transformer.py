"""
    Main module for the frame transformer.
    TODO: Pre-transforms and post-transforms are not included. e.g. in Airsim, NED coordinates ignore initial yaw.
"""
import numpy as np
from typing import Callable, Tuple

from frame_transformer.transformations import _transform
from frame_transformer.explains import _explain, _explain_system
from frame_transformer.systems import System, SYSTEM_DICT
from frame_transformer.frames import Frame

class FrameTransformer:
    def __init__(self, origin: System, target: System):
        """
            Initializes the transformer from two systems.
            Args:
                origin: The origin system.
                target: The target system.
        """
        self.origin_system = origin
        self.target_system = target
        try:
            self.origin = SYSTEM_DICT[origin]
        except KeyError:
            print(f"System {origin} not found.")

        try:
            self.target = SYSTEM_DICT[target]
        except KeyError:
            print(f"System {target} not found.")

    @classmethod
    def from_frames(cls, origin: Frame, target: Frame):
        """
            Sets up the transformer from two frames.
            Systems will be None.
            Args:
                origin: The origin frame.
                target: The target frame.
        """
        # Make up the systems and remove them
        transformer = cls(origin.system, target.system)
        transformer.origin = origin
        transformer.target = target
        transformer.origin_system = None
        transformer.target_system = None
        return transformer
        

    def transform(self, translation: np.ndarray, rotation: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
            Transforms a pose from one frame to another.
            Args:
                translation: The translation vector of the pose in the origin frame.
                rotation: The rotation matrix (3x3) or quaternion (4x1) of the pose in the origin frame.
            Returns:
                The translation vector and quaternion of the pose in the target frame.
        """
        return _transform(translation, rotation, self.origin, self.target)

    def explain(self) -> None:
        """
            Explains the transformation from one frame to another.
        """
        if self.origin_system is not None and self.target_system is not None:
            _explain_system(self.origin_system, self.target_system)
        _explain(self.origin, self.target)

    