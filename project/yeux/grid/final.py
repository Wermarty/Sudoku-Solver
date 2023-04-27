import pathlib
import numpy as np
from numpy import cos, sin

import skimage.transform as skt

from yeux.grid import utils, rotate_image, detect_grid, get_cases


def read_grid(img,taille_case) : 
    theta = rotate_image.find_rotation(img,0)
    rotated = rotate_image.rotate(img,0)
    coord = detect_grid.detect_grid(rotated,0,0,0)
    grid = get_cases.getcases(rotated,coord,taille_case)
    
    return grid,theta


def estimate_trans(img, theta):
    rows, cols = img.shape[0], img.shape[1]
    center = np.array((cols, rows)) / 2. - 0.5
    T_center = np.eye(3)
    T_center[:2, 2] = center
    
    T_center_inv = np.eye(3)
    T_center_inv[:2, 2] = - center
    angle = np.deg2rad(theta)
    R = np.asarray([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    T_rot = np.eye(3)
    T_rot[:2, :2] = R
    T = T_center @ T_rot @ T_center_inv
    
    # find the translation after the resize
    corners = np.array([
            [0, 0, 1],
            [0, rows - 1, 1],
            [cols - 1, rows - 1, 1],
            [cols - 1, 0, 1]
        ])
    corners = corners @ np.linalg.inv(T).T
    minc = corners[:, 0].min()
    minr = corners[:, 1].min()
    
    translation = np.asarray([minc, minr])
    T_trans = np.eye(3)
    T_trans[:2, 2] = translation
    T = T @ T_trans
        
    return T[:2, :2], T[:2, 2]

def get_coordinates_cases(img):
    theta = rotate_image.find_rotation(img,0)
    #print(theta)
    rotated = rotate_image.rotate(img,0)
    
    R, t = estimate_trans(img, theta)
    coord = detect_grid.detect_grid(rotated,0,0,0)
    
    coordx = coord[0,0::2]
    coordy = coord[1,0::2]    
    
    size_case = np.mean(coordx[1:]-coordx[:-1])
    
    
    
    temp = np.asarray([[i,j] for j in coordy for i in coordx ])
    
    res=[]
    res = (temp @ R.T + t).astype(int)
    
    res = res.reshape((9,9,2))
    
    return (size_case,res)

if __name__ == "__main__":

    im = utils.read(pathlib.Path("../grille sudoku/9.jpg"))
    utils.iprint(im)
    
    #rotated = rotate_image.rotate(im,0)
    #coord = (detect_grid.detect_grid(rotated,0,0,0)).T.astype(int)
    #detect_grid.print_coord_img(rotated, coord)
    #facteur_resize = im.shape[0]/rotated.shape[0]
    #print(facteur_resize)
    
    res = get_coordinates_cases(im)

    
    detect_grid.print_coord_img(im, res[1].reshape((81,2)))
    


    
    
    
    
