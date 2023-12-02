"""
    Code to define the systems.
"""
from typing import Literal

System = Literal[
        "ros",
        "opencv",
        "airsim",
    ]
"""
    System type to integrate all the programs.
    They are included and mapped to a Frame type.
"""

SYSTEM_DICT = {
    "ros": "x_yl_zu",
    "opencv": "z_xr_yd",
    "airsim": "x_yr_zd",
}
"""
    Dictionary that maps a system to a frame.
"""