import sys
import pathlib
from matplotlib import pyplot as plt 

from code_number import import_data_model,find_orientation,number_recognition,write_sudoku
from code_grid import final
from code_grid import utils
from code_grid import detect_grid
from drawer import drawer

def find_number(cases, tab_num_model, orientation_initial):
    orientation_modif = find_orientation(cases,tab_num_model)
    tab_num_find = number_recognition(cases, tab_num_model, orientation_modif)
    write_sudoku(tab_num_find)
    
    return orientation_initial - orientation_modif

img = utils.read("sudoku.jpg")
if(img is None):
    print("can't read images")
    exit()

pixel_resize = 20

print("starting grid detection", end=" - ")

[cases,theta] = final.read_grid(img,pixel_resize)

print("OK")

tab_num_model = import_data_model(pixel_resize)


print("starting number detection", end=" - ")

orientation = find_number(cases,tab_num_model, theta)

print("OK")
    


print("starting writing phase", end=" - ")

def Ryan():
    print("bouge toi mon salop")
    return 1, 1

case_size, coords = Ryan()
drawer.draw(case_size, coords)

print("OK")
