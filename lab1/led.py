import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
light = 4
GPIO.setup(light, GPIO.OUT)

while 1:
    GPIO.output(light, True)
    time.sleep(1)
    GPIO.output(light, False)
    time.sleep(1)
