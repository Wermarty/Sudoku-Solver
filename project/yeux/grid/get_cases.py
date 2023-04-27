
import numpy as np
import cv2
import matplotlib.pyplot as plt

from yeux.grid import detect_grid
from yeux.grid import utils



def getcase_ij(img,coord,i=0,j=0,eps=3):
    # ligne i, colonne j
    x= coord[0,:]
    y= coord[1,:]
    case = img[y[2*j]+eps:y[2*j+1]-eps,x[2*i]+eps:x[2*i+1]-eps]
    
    return case
    
def clean_case(case,len_kernel=3):
    th,case=cv2.threshold(case,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
    #case = (case<50).astype(np.uint8)
    utils.iprint(case)

    kernel = np.ones((len_kernel,1))
    case = cv2.morphologyEx(case, cv2.MORPH_CLOSE, kernel)
    utils.iprint(case)
    case = cv2.morphologyEx(case, cv2.MORPH_CLOSE, kernel.T)
    utils.iprint(case)
    return case



    

def getcases(img,coord,taille_case=30,eps=3):
    grid=[]
    for j in range(9):
        for i in range(9):
            grid.append(
                
                cv2.resize (getcase_ij(img,coord,i,j,eps), dsize=(taille_case,taille_case) ) ) 
            
    grid=np.array(grid)
    #breakpoint()
    grid=np.reshape(grid,(9,9,taille_case,taille_case))
 
    
    
    return grid     


def print_grid(grid:np.ndarray):
    plt.figure()
    for i in range(9):
        for j in range(9):
            plt.subplot(9,9,9*i+j+1)
            plt.axis("off")
            plt.imshow(grid[i][j])
    plt.show()

def get_parser():
    parser = utils.get_base_parser("detect grid")
    return parser

if __name__ == "__main__":
    parser = get_parser()
    parser.add_argument("--ligne", help="ligne", type=int)
    parser.add_argument("--colonne", help="colonne", type=int)


    args = parser.parse_args()
    img = utils.read(args.input)
    
    coord = detect_grid.detect_grid(img, 0,0,0)
    l=args.ligne
    if(l==None):
        l=0
    c=args.colonne
    if(c==None):
        c=0
        
    
    case = getcase_ij(img, coord, l, c)
    grid = getcases(img, coord)
    print_grid(grid)    
    
    
    



