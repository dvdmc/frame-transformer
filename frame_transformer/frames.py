"""
    Code to define the frames.
"""
from typing import Literal

Frame = Literal[
        "x_yl_zu", # Right-handed
        "x_yl_zd", # Left-handed
        "x_yr_zu", # Left-handed
        "x_yr_zd", # Right-handed
        "x_zl_yu", # Left-handed
        "x_zl_yd", # Right-handed
        "x_zr_yu", # Right-handed
        "x_zr_yd", # Left-handed

        "y_xl_zu", # Left-handed
        "y_xl_zd", # Right-handed
        "y_xr_zu", # Right-handed
        "y_xr_zd", # Left-handed
        "y_zl_xu", # Right-handed
        "y_zl_xd", # Left-handed
        "y_zr_xu", # Left-handed
        "y_zr_xd", # Right-handed
        
        "z_xl_yu", # Right-handed
        "z_xl_yd", # Left-handed
        "z_xr_yu", # Left-handed
        "z_xr_yd", # Right-handed
        "z_yl_xu", # Left-handed
        "z_yl_xd", # Right-handed
        "z_yr_xu", # Right-handed
        "z_yr_xd", # Left-handed
    ]
"""
    Frame type. It is redundant but easier to read.
"""

HAND_DICT = {
    "x_yl_zu": "r",
    "x_yl_zd": "l",
    "x_yr_zu": "l",
    "x_yr_zd": "r",
    "x_zl_yu": "l",
    "x_zl_yd": "r",
    "x_zr_yu": "r",
    "x_zr_yd": "l",

    "y_xl_zu": "l",
    "y_xl_zd": "r",
    "y_xr_zu": "r",
    "y_xr_zd": "l",
    "y_zl_xu": "r",
    "y_zl_xd": "l",
    "y_zr_xu": "l",
    "y_zr_xd": "r",
    
    "z_xl_yu": "r",
    "z_xl_yd": "l",
    "z_xr_yu": "l",
    "z_xr_yd": "r",
    "z_yl_xu": "l",
    "z_yl_xd": "r",
    "z_yr_xu": "r",
    "z_yr_xd": "l",
}
"""
    Dictionary that maps a frame to a hand.
"""