# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 22:47:57 2023

@author: horry
"""

import numpy as np
import cv2

from code_grid import utils

def find_size_square(lines,axis=0, filter_min_size: float = 10):

    coord = lines[:,0,axis]
    list_x2 = np.sort(coord)
    dist = list_x2[1:] - list_x2[:-1]
    dist = dist[dist > filter_min_size]
    return np.median(dist)

def filter_coord(lines: np.ndarray, size: float, axis:int = 0, eps: float = 10):
    tab_coord = np.sort(lines[:,0,axis])
    dists = tab_coord[1:] - tab_coord[:-1]
    res= []
    for i,d in enumerate(dists):
        if(size-eps < d < size+eps):
            res.append(tab_coord[i])
            res.append(tab_coord[i+1])
    return (np.asarray(res)).astype("uint32")
          

"""
def filter_line(lines: np.ndarray, size: float, axis:int = 0, eps: float = 10):
    res = []

    for line in lines:
        dists = np.abs(lines[:, 0, axis] - line[0, axis])
        dists = dists[dists > 5]
        if len(dists) > 0:
            if dists.min() > size - eps and dists.min() < size + eps:
                res.append(line)
    return np.asarray(res)
"""
        
def print_grid_img(img: np.ndarray, coordx:np.ndarray, coordy:np.ndarray):
    img_copy = cv2.cvtColor(np.copy(img),cv2.COLOR_GRAY2RGB)
    blank = np.zeros_like(img_copy)
    
    h,l = np.shape(img)

    for x in coordx:
        cv2.line(img_copy,(x,0),(x,h), color=(255, 0, 0), thickness=1)
        cv2.line(blank,(x,0),(x,h), color=(255, 0, 0), thickness=1)
        
    for y in coordy:
        cv2.line(img_copy,(0,y),(l,y), color=(255, 0, 0), thickness=1)
        cv2.line(blank, (0,y),(l,y), color=(255, 0, 0), thickness=1)

    utils.iprint(np.vstack((img_copy, blank)))
    
def print_line_img(img: np.ndarray, lines :np.ndarray):
    img_copy = cv2.cvtColor(np.copy(img),cv2.COLOR_GRAY2RGB)
    blank = np.zeros_like(img_copy)
    for line in lines :
        x2,y2,x1,y1=line[0]
        cv2.line(img_copy,(x2,y2),(x1,y1), color=(255, 0, 0), thickness=1)
        cv2.line(blank,(x2,y2),(x1,y1), color=(255, 0, 0), thickness=1)

def print_coord_img(img:np.ndarray,coord:np.ndarray):
    img_copy = np.copy(img)
    for c in coord :
        cv2.circle(img_copy,c,1,(255,0,0),1)
    utils.iprint(img_copy)
 
def getimage_grid(img,grid):
    img_copy = cv2.cvtColor(np.copy(img),cv2.COLOR_GRAY2RGB)
    blank = np.zeros_like(img_copy)
    h,l = np.shape(img)
    for x in grid[0]:
        cv2.line(img_copy,(x,0),(x,h), color=(255, 0, 0), thickness=1)
        cv2.line(blank,(x,0),(x,h), color=(255, 0, 0), thickness=1)
        
    for y in grid[1]:
        cv2.line(img_copy,(0,y),(l,y), color=(255, 0, 0), thickness=1)
        cv2.line(blank, (0,y),(l,y), color=(255, 0, 0), thickness=1)
    res = np.vstack((img_copy,blank))
    return res

def getimage_lines(img: np.ndarray,lines : np.ndarray):
    img_copy = cv2.cvtColor(np.copy(img),cv2.COLOR_GRAY2RGB)
    for line in lines :
        x2,y2,x1,y1=line[0]
        cv2.line(img_copy,(x2,y2),(x1,y1), color=(255, 0, 0), thickness=1)
    return img_copy

def detect_grid(img: np.ndarray,is_plot_edges: bool,is_plot_grid:bool, is_plot_coord:bool):
    
    linesx, linesy = utils.detect_hough_line_sobel(img, is_plot_edges)
    sizex,sizey = find_size_square(linesx,axis=0),find_size_square(linesy,axis=1)
    coordx = filter_coord(linesx, sizex,axis=0)
    coordy = filter_coord(linesy, sizey,axis=1)
    
    
    
    if(is_plot_grid):    
        print_grid_img(img, coordx, coordy)
        
    
    coord = [(i,j) for i in coordx for j in coordy]
    if(is_plot_coord):    
        print_coord_img(img, coord)
    
    return np.asarray([coordx,coordy])
    
    
    
    

def get_parser():
    parser = utils.get_base_parser("detect grid")
    return parser



if __name__ == "__main__":
    parser = get_parser()
    parser.add_argument("--print-edges", help="print the edges", action="store_true")
    parser.add_argument("--print-grid", help="print the grid", action="store_true")
    parser.add_argument("--print-coord", help="print the coord", action="store_true")


    args = parser.parse_args()
    img = utils.read(args.input)
    
    grid = detect_grid(img, args.print_edges,args.print_grid,args.print_coord)