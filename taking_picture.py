from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

butPin = 3


GPIO.setmode(GPIO.BOARD)
GPIO.setup(butPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

camera = PiCamera()
# camera.resolution = (512, 400)

camera.start_preview()

taken = False
while not taken:
    if not GPIO.input(butPin):
        taken = True
        camera.capture("button_test.jpg")
    else:
        sleep(0.3)


GPIO.cleanup()
camera.stop_preview()