# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 22:50:50 2023

@author: horry
"""

import argparse
import pathlib
from typing import Optional

import cv2
import matplotlib.pyplot as plt
import numpy as np

def get_base_parser(desc: str):
    parser = argparse.ArgumentParser(desc)
    parser.add_argument("--input", "-i", help="input image in jpg por png", type=pathlib.Path)
    parser.add_argument("--output", "-o", help="output directory", type=pathlib.Path, default=None)
    return parser

def read(path: pathlib.Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if(img is None):
        print("can't read the img")
        return None
    
    return img.astype(np.uint8)

def iprint(img: np.ndarray):
    """plot an image

    Parameters
    ----------
    img : np.ndarray
        img to plot

    Returns
    -------
    None.

    """
    plt.figure()
    plt.imshow(img,cmap='gray')
    plt.show()

def get_output_path(
        input_path: pathlib.Path,
        suffix: str="_rotated",
        out: Optional[pathlib.Path]=None) -> pathlib.Path:
    """Get the proper output path given the input path and a suffix.
    
    If the out path is None, then the directory of the output will be the input
    directory. The results has the same name as the input path but a suffix is 
    added
    

    Parameters
    ----------
    input_path : pathlib.Path
        path of the input
    suffix : str, optional
        suffix to add to the output name. The default is "_rotated".
    out : Optional[pathlib.Path], optional
        output dir if None, the output dir is the input dir. The default is
        None.

    Returns
    -------
    pathlib.Path
        Path of the output file

    """
    output_path = input_path.parent
    output_name = input_path.stem + suffix
    output_suffix = input_path.suffix
    if out is not None:
        output_path = out
        output_path.mkdir(parents=True, exist_ok=True)
    return output_path / f"{output_name}{output_suffix}"



def detect_hough_line_canny(img: np.ndarray,is_plot_edges: bool =0) -> np.ndarray:
    """
    Detect the lines in an image using canny edges detector

    Parameters
    ----------
    img : np.ndarray
        input image.
    is_plot_edges : bool
        do we plot the edges or not.

    Returns
    -------
    lines : np.ndarray
        Detected lines

    """
    edges = cv2.Canny(img, 50, 200)
    if is_plot_edges:
        iprint(edges)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 150, minLineLength=100, maxLineGap=250)
    return lines




def detect_hough_line_sobel(img: np.ndarray,is_plot_edges: bool=0,len_kernel:int =40):

        kernel = np.ones((len_kernel,1))
        
        edgesx = cv2.Sobel(img,-1,1,0,ksize=3)
        edgesx = (edgesx > 128).astype(np.uint8)        
        edgesx = cv2.morphologyEx(edgesx, cv2.MORPH_OPEN, kernel)
        
        edgesy = cv2.Sobel(img,-1,0,1,ksize=3)
        edgesy = (edgesy > 128).astype(np.uint8)
        edgesy = cv2.morphologyEx(edgesy, cv2.MORPH_OPEN, kernel.T)

        if is_plot_edges:
            iprint(np.vstack((edgesx, edgesy)))
        
        linesx = cv2.HoughLinesP(edgesx, 1, 5*np.pi/180, 50, minLineLength=100, maxLineGap=250)
        linesy = cv2.HoughLinesP(edgesy, 1, 5*np.pi/180, 50, minLineLength=100, maxLineGap=250)
        
        return linesx, linesy
            