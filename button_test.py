import RPi.GPIO as GPIO
from time import sleep

ledPin = 7


GPIO.setmode(GPIO.BOARD)

# GPIO.setup(2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT)
try:
   while 1:
     # etat = GPIO.input(2)

    # if etat == 0:
    #     GPIO.output(ledPin, True)
    #     print("izi")

    # else:
    #     GPIO.output(ledPin, False)
    #     print("not izi")
 
    
        sleep(0.5)
        GPIO.output(ledPin, GPIO.LOW)
        print("zi")
        sleep(0.5)
        GPIO.output(ledPin, GPIO.HIGH)
        print("not izi")

except:
    GPIO.cleanup()



