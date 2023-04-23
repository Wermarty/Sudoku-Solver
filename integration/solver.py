import sys
import pathlib
from matplotlib import pyplot as plt 

from code_number import import_data_model,find_orientation,number_recognition,write_sudoku
from code_grid import final
from code_grid import utils
from code_grid import detect_grid
from drawer import draw

def find_number(cases, tab_num_model, orientation_initial):
    orientation_modif = find_orientation(cases,tab_num_model)
    tab_num_find = number_recognition(cases, tab_num_model, orientation_modif)
    write_sudoku(tab_num_find,"sudoku_to_resolve", "")
    
    return orientation_initial - orientation_modif

img = utils.read("sudoku.jpg")
if(img is None):
    print("can't read images")
    exit()

pixel_resize = 20

print("starting grid detection", end=" - ")

[cases,theta] = final.read_grid(img,pixel_resize)

print("OK")

if(args.output == None):
    output_path = pathlib.Path().absolute() 
else:
    directory_path = pathlib.Path(args.output)

    if not directory_path.exists():
        directory_path.mkdir(parents=True)
    output_path = args.output
    print(output_path)



tab_num_model = import_data_model(pixel_resize)
if(args.name is None):
    name = "toresolve"   
else :
    name = args.name

print("starting number detection", end=" - ")

orientation = find_number(cases,tab_num_model, theta)

print("OK")
    


print("starting writing phase", end=" - ")

def Ryan():
    print("bouge toi mon salop")
    return 1, 1

case_size, coords = Ryan()
draw(case_size, coords)

print("OK")
