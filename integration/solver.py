import sys
import pathlib
import os
from time import sleep
from matplotlib import pyplot as plt
from picamera import PiCamera

from code_number import import_data_model,find_orientation,number_recognition,write_sudoku
from code_grid import final
from code_grid import utils
from code_grid import detect_grid
from drawer import drawer, initialise

capture = False
ryan = False
hugo = False
marcelin = False
benjamin = False

def find_number(cases, tab_num_model, orientation_initial):
    orientation_modif = find_orientation(cases,tab_num_model)
    tab_num_find = number_recognition(cases, tab_num_model, orientation_modif)
    write_sudoku(tab_num_find)

    return orientation_initial - orientation_modif

capture = True
ryan = True
hugo = True
marcelin = True
benjamin = True

initialise.initialise()

if capture:
    camera = PiCamera()
    camera.capture("sudoku.jpg")

img = utils.read("sudoku.jpg")
if(img is None):
    print("can't read images")
    exit()

pixel_resize = 40

print("starting grid detection", end=" - ")
if ryan:
    [cases,theta] = final.read_grid(img,pixel_resize)
print("OK")



print("starting number detection", end=" - ")
if hugo:
    tab_num_model = import_data_model(pixel_resize)
    orientation = find_number(cases,tab_num_model, theta)
print("OK")



print("starting solver", end=" - ")
if marcelin:
    os.system("./solver")
    sleep(1)
print("OK")


print("starting writing phase", end=" - ")
if benjamin:
    case_size, coords = final.get_coordinates_cases(img)
    drawer.draw(case_size, coords)
print("OK")
