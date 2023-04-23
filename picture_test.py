from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(4)
camera.stop_preview()


camera.capture("sudoku_5.jpg")

