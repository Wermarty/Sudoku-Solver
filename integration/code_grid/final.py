import pathlib
import numpy as np
from numpy import cos, sin

import skimage.transform as skt

from code_grid import utils
from code_grid import rotate_image
from code_grid import detect_grid
from code_grid import get_cases



def read_grid(img,taille_case) : 
    theta = rotate_image.find_rotation(img,0)
    rotated = rotate_image.rotate(img,0)
    coord = detect_grid.detect_grid(rotated,0,0,0)
    grid = get_cases.getcases(rotated,coord,taille_case)
    
    return grid,theta

def get_coordinates_cases(img):
    theta = rotate_image.find_rotation(img,0)
    print(theta)
    rotated = rotate_image.rotate(img,0)
    coord = detect_grid.detect_grid(rotated,0,0,0)
    
    coordx = coord[0,0::2]
    coordy=coord[1,0::2]    
    
    temp = [(i,j) for i in coordx for j in coordy]
    res=[]
    center = tuple(map(lambda x: x/2, img.shape[:2]))
    for point in temp :
        x= int( ( cos(theta)*(point[0]-center[0]) + center[0]  - sin(theta) *(point[1]-center[1]) ) )
        y =int( (sin(theta)*(point[0]-center[0])+ center[1] + cos(theta)*(point[1]-center[1]))  )
        
        res.append( (x   ,  y) )   
        
    return res
    
"""
im = utils.read(pathlib.Path("../grille sudoku/4.jpg"))
utils.iprint(im)
rotated = rotate_image.rotate(im,0)
facteur_resize = im.shape[0]/rotated.shape[0]
print(facteur_resize)
coord = get_coordinates_cases(im,facteur_resize)

detect_grid.print_coord_img(im,coord)

"""
    
    
    
    
