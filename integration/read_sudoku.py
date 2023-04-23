import sys
import pathlib
from matplotlib import pyplot as plt 

from code_number import import_data_model,find_orientation,number_recognition,write_sudoku,plot_num_model
from code_grid import final
from code_grid import utils
from code_grid import detect_grid


def find_number(cases, tab_num_model, orientation_initial, name_sudoku_text, path_to_write):
    orientation_modif = find_orientation(cases,tab_num_model)
    tab_num_find = number_recognition(cases, tab_num_model, orientation_modif)
    write_sudoku(tab_num_find,name_sudoku_text, path_to_write)
    
    return orientation_initial - orientation_modif



if __name__ == "__main__":
    parser = utils. get_base_parser("read_sudoku")
    parser.add_argument("--size-case", help="size of the resized images of each case. 20 by default ", type=int)
    parser.add_argument("--name",help=" name of the output file ", type=str)
    args = parser.parse_args()

    img = utils.read(args.input)
    if(img is None):
        print("can't read images")
        exit()
    
    pixel_resize = 20

    if(args.size_case is not None):
        pixel_resize = args.size_case

    [cases,theta] = final.read_grid(img,pixel_resize)
    
    img = cases[0,3]
    plt.figure()
    plt.imshow(img)
    plt.savefig("img")
    
    img = cases[1,1]
    plt.figure()
    plt.imshow(img)
    plt.savefig("img2")
    
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
    
    #plot_num_model(tab_num_model,1)
    #detect_grid.print_grid_img(cases)
    
    orientation = find_number(cases,tab_num_model, theta, name,output_path)
    
    
    
