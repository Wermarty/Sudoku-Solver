import sys
import os
from time import sleep
from picamera import PiCamera

#sys.path.insert(0, '/yeux/grid/')
#sys.path.insert(1, '/yeux/number')

from yeux.grid import final, utils, detect_grid
from yeux.number.code_number import import_data_model, find_orientation, number_recognition, write_sudoku
from bras.drawer import draw, initialise

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

initialise()

if capture:
    camera = PiCamera()
    camera.capture("generated_data/sudoku.jpg")

img = utils.read("generated_data/sudoku.jpg")
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
    ooorientation = find_number(cases,tab_num_model, theta)
print("OK")



print("starting solver", end=" - ")
if marcelin:
    os.system("./cerveau/solver")
    sleep(1)
print("OK")


print("starting writing phase", end=" - ")
if benjamin:
    case_size, coords = final.get_coordinates_cases(img)
    draw(case_size, coords)
print("OK")
