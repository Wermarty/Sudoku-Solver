# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 18:39:40 2023
@author: hugob
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from skimage import transform 
from skimage import filters
import random
from pathlib import Path
from skimage import io
from skimage import img_as_float
from skimage.color import rgb2gray

def import_data_model(taille_case):
    data = Path().cwd() / 'data' / 'data_train' / 'num_police2bis'
    k = 1
    tab_num_model = []
    for f in sorted(list(data.rglob("*.jpg"))):
        img = rgb2gray(img_as_float(io.imread(f))) #Normalization
        img = transform.resize((img - np.mean(img))/np.std(img),(taille_case,taille_case)) #Standardization
        tab_num_model.append((img,k,0)) # Reference images
        tab_num_model.append((transform.rotate(img,90),k,90))
        tab_num_model.append((transform.rotate(img,180),k,180))
        tab_num_model.append((transform.rotate(img,270),k,270))
        k += 1
    return tab_num_model

def img_is_empty(img):
    nbr_pixel_to_delete = round(img.shape[0]*0.1)
    if (np.mean(filters.sobel(img[nbr_pixel_to_delete:img.shape[0]-nbr_pixel_to_delete,nbr_pixel_to_delete:img.shape[1]-nbr_pixel_to_delete ]))) < 0.02 : 
        return True # Regarde si l'image contient des HF
    else : 
        return False

# Trouve l'orientation de l'image
def find_orientation(tab_num_to_reco, tab_num_model):
    possible_orientation = [0,90,180,270] # Differente orientations testées
    tab_orientation = []
    
    for i in range(tab_num_to_reco.shape[0]):
        for j in range(tab_num_to_reco.shape[1]):
            if (img_is_empty(tab_num_to_reco[i,j,:,:]) == True) : # Si image vide on passe à la suivante
                continue
            
            max_inter_corr = 0
            
            # Corrélation pour chaque img de tab_num_to_reco avec tab_num_model
            for k in range(len(tab_num_model)):
                inter_corr = scipy.signal.correlate(tab_num_to_reco[i,j,:,:],tab_num_model[k][0],mode = 'same',method='fft') 
                test = np.max(inter_corr)
                if test > max_inter_corr :
                    max_inter_corr = test
                    orientation = tab_num_model[k][2]
            tab_orientation.append(orientation)
        
    nbr_occurence = (tab_orientation.count(0),tab_orientation.count(90),tab_orientation.count(180),tab_orientation.count(270))
    orientation_f = possible_orientation[nbr_occurence.index(max(nbr_occurence))]
    return orientation_f


def number_recognition(tab_num_to_reco, tab_num_model, orientation):
    possible_orientation = [0,90,180,270]
    tab_to_return = np.zeros((tab_num_to_reco.shape[0],tab_num_to_reco.shape[1]))
    for i in range(tab_num_to_reco.shape[0]):
        for j in range(tab_num_to_reco.shape[1]):
            if (img_is_empty(tab_num_to_reco[i,j,:,:]) == True) : # Si image vide numéro trouvé égale 0
                continue
        
            max_inter_corr = 0
            for k in range(possible_orientation.index(orientation),len(tab_num_model),4):
                img = np.copy(tab_num_to_reco[i,j,:,:])
                img = (img- np.mean(img))/np.std(img)
                inter_corr = scipy.signal.correlate(img,tab_num_model[k][0],mode = 'same',method='fft')  
                test = np.max(inter_corr)
                if test > max_inter_corr :
                    num = tab_num_model[k][1]
                    max_inter_corr = test
           
            if (orientation == 0):
                tab_to_return[i,j] = num
            elif (orientation == 90):
                tab_to_return[j,8-i] = num       
            elif (orientation == 180):
                tab_to_return[8-i,8-j] = num
            elif (orientation == 270):
                tab_to_return[8-j,i] = num    
            else:
                print("erreur orientation\n")
            
                    
    return tab_to_return


# Ecriture dans un .txt des numéro trouvé dans tab_num_find
def write_sudoku(tab_num_find,name_sudoku,path_to_write):
    name_sudoku = name_sudoku + '.txt'
    sudoku_txt = open(path_to_write / name_sudoku ,"w")
    
    for row in range(tab_num_find.shape[0]):
        for colum in range(tab_num_find.shape[1]):
            char = str(round(tab_num_find[row,colum]))
            sudoku_txt.write(char) 
        sudoku_txt.write("\n")
    
    sudoku_txt.close()


def plot_num_model(tab_model,i):
    plt.figure(i)
    plt.title("Model number")
    z = 1
    for k in range(0,36,4):
        plt.subplot(3,3,z)
        plt.imshow(tab_model[k][0])
        plt.title(str(k))
        z+=1
        
def plot_9nums_test(tab_num_test,i):
    len_ = len(tab_num_test)-1
    plt.figure(i)
    plt.title("Test number")
    for i in range(9):
        k = random.randint(0,len_)
        plt.subplot(3,3,i+1)
        plt.imshow(tab_num_test[k][0])