# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 21:41:05 2023

@author: horry
"""
import argparse
import pathlib
import time
from typing import Optional

import cv2
import matplotlib.pyplot as plt
import numpy as np
import skimage
import skimage.transform as skt

from code_grid import utils


def find_angle_lines(lines: np.ndarray) -> float:

    array_angle = np.round(np.degrees((np.arctan2( lines[:,0,1]-lines[:,0,3] , lines[:,0,0]-lines[:,0,2] )))%90,2) 
    max_angle_count = 0
    for ang in array_angle:
        if(max_angle_count < np.count_nonzero(array_angle == ang) ):
            max_angle_count = np.count_nonzero(array_angle == ang) 
            angle = ang
    return angle

def find_rotation(img: np.ndarray, is_plot_edges: bool) -> float:
    """find the rotation of an image

    Args:
        img (np.ndarray): _description_
        is_plot_edges (bool): _description_

    Returns:
        float: _description_
    """
    lines = utils.detect_hough_line_canny(img, is_plot_edges)
    angle = find_angle_lines(lines)
    return angle

def rotate(img: np.ndarray, is_plot_edges: bool) -> np.ndarray:
    """
    Given an angle rotate the image correctly

    Parameters
    ----------
    img : np.ndarray
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    angle = find_rotation(img, is_plot_edges)
    rotated = skt.rotate(img, angle,resize=True)
    return (256*rotated).astype(np.uint8) 
    
    

if __name__ == "__main__":
    parser = utils.get_base_parser("Function to rotate a file")
    parser.add_argument("--save-edges", help="save the edges", action="store_true")
    args = parser.parse_args()
    # read image
    img = utils.read(args.input)
    t = time.time()
    rotated = rotate(img, args.save_edges)
    print(f" time to rotate: {time.time() - t}")
    out_path = utils.get_output_path(args.input, "_rotated", args.output)
    cv2.imwrite(str(out_path), rotated)
        
    