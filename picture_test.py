from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.stop_preview()

camera.resolution = (512, 384)

camera.capture("sudoku_5.jpg")

