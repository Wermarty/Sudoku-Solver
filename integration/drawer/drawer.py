import serial
from time import sleep
from IOmanager import IOmanager
from serWriter import serWriter

def get_inc(i, j):
     return j if (i%2 != 1) else 8-j

def dist2time(x):
    return 0.1 * x

def get_time(x, x_last, y, y_last):
    time_serial = 0.5
    time_number = 1.70

    x_dist, y_dist = abs(x-x_last), abs(y-y_last)

    time_travel = dist2time(x_dist) + dist2time(y_dist)

    return time_serial + time_travel + time_number


def get_good_coord(bad_coord):
    good_coord = []
    for i in range(len(bad_coord)):
        temp = []
        for j in range(len(bad_coord[i])):
            coord = []
            for k in range(len(bad_coord[i][j])):
                coord.append(bad_coord[i][j][k]/2)
            temp.append(coord)
        good_coord.append(temp)

    return good_coord





def draw(case_size, coords):

    Io = IOmanager()
    write_on_ser = serWriter(ser)

    port = "/COM3"
    ser = serial.Serial(port, 9600)
    ser.reset_input_buffer()

    
    x_origin, y_origin = Io.get_origin()
    sudoku = Io.sudoku()

    write_on_ser.draw(0, 0, 0)
    sleep(0.5)
    write_on_ser.reset()
    sleep(5)
    write_on_ser.init(case_size)

    x_last, y_last = x_origin, y_origin    
    for i in range(len(sudoku)):
        for k in range(len(sudoku[i])):
            j = get_inc(i, k)
            if (sudoku[i][j] != 0) :
                x, y = coords[i][j][1], coords[i][j][0]
                number = sudoku[i][j]

                write_on_ser.draw(number, y, x)
                
                sleep(get_time(x, x_last, y, y_last))
                
                x_last, y_last = x, y

    sleep(5)