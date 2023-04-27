import serial

from time import sleep
from drawer import serWriter

def initialise():
    port = "/dev/ttyACM0"
    ser = serial.Serial(port, 9600)
    ser.reset_input_buffer()

    write_on_ser = serWriter.serWriter(ser)
    write_on_ser.draw(0,0,0)
    sleep(2)

    write_on_ser.reset()
    sleep(7)
