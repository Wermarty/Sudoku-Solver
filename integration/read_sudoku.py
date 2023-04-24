import sys
import pathlib
import time

from code_number import import_data_model,find_orientation,number_recognition,write_sudoku,plot_num_model
from code_grid import final
from code_grid import utils
from code_grid import detect_grid
from code_grid import get_cases


def find_number(cases, tab_num_model, orientation_initial, name_sudoku_text, path_to_write):
    orientation_modif = find_orientation(cases,tab_num_model)
    tab_num_find = number_recognition(cases, tab_num_model, orientation_modif)
    write_sudoku(tab_num_find,name_sudoku_text, path_to_write)
    
    return orientation_initial - orientation_modif



if __name__ == "__main__":
    
    t = time.time()
    
    parser = utils. get_base_parser("read_sudoku")
    parser.add_argument("--size-case", help="size of the resized images of each case. 20 by default ", type=int)
    args = parser.parse_args()

    input = "sudoku.jpg"
    if(args.input is not None):
        input = args.input
        
    img = utils.read(input)
    if(img is None):
        print("can't read images")
        exit()
    
    pixel_resize = 20

    if(args.size_case is not None):
        pixel_resize = args.size_case

    [cases, theta] = final.read_grid(img, pixel_resize)   
    
    print(f" cases sucessufully isolated, in : {round(time.time() - t,2)} s")
    
    output_path = pathlib.Path().absolute() 
    name = "sudoku_toresolve"
    
    if args.output is not None:
        out = pathlib.Path(args.output)
        output_path = out.parent
        output_path.mkdir(parents=True, exist_ok=True)
        name = out.stem
            
     
    tab_num_model = import_data_model(pixel_resize)
    
    orientation = find_number(cases,tab_num_model, theta, name,output_path)
    print(f" sudoku sucessfully read , in : {round(time.time() - t,2)} s")

    print(f"save in {output_path} in the file {name}.txt")

    
