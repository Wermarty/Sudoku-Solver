import serial
import numpy as np
from drawer import IOmanager
from drawer import serWriter

from time import sleep

def get_inc(i, j):
    return j if (i%2 != 1) else 8-j

def dist2time(x):
    return 0.1 * x

def pixel_to_cm(pixel):
    return pixel * 1.25 / 68

def get_time(x, x_last, y, y_last):
    time_serial = 0.5
    time_number = 1.70

    x_dist, y_dist = abs(x-x_last), abs(y-y_last)

    time_travel = dist2time(x_dist) + dist2time(y_dist)

    return time_serial + time_travel + time_number


def get_cm_coords(bad_coord):
    good_coord = np.ndarray((9, 9, 2))
    for i in range(len(bad_coord)):
        for j in range(len(bad_coord[i])):
            good_coord[i, j, 0] = pixel_to_cm(1920 - bad_coord[j,8-i][0])
            good_coord[i, j, 1] = pixel_to_cm(bad_coord[j,i][1])

    return good_coord





def draw(case_size, coords):

    port = "/COM3"
    #ser = serial.Serial(port, 9600)
    #ser.reset_input_buffer()

    Io = IOmanager.IOmanager()
    #write_on_ser = serWriter.serWriter(ser)

    x_origin, y_origin = Io.origin()
    sudoku = Io.sudoku()

    cm_coords = get_cm_coords(coords)
    print(cm_coords[0,0])
    #write_on_ser.draw(0, 0, 0)
    #sleep(0.5)
    #write_on_ser.reset()
    #sleep(5)
    #write_on_ser.init(case_size)

    #x_last, y_last = x_origin, y_origin
    #for i in range(len(sudoku)):
    #    for k in range(len(sudoku[i])):
    #        j = get_inc(i, k)
    #        if (sudoku[i][j] != 0) :
    #            #x, y = coords[i][j][1], coords[i][j][0]
    #            #number = sudoku[i][j]
    #            #write_on_ser.draw(number, y, x)
    #            #sleep(get_time(x, x_last, y, y_last))
    #            #x_last, y_last = x, y
    #            j = 2
    #        j = 1
    #    j = 1
    #sleep(5)
