import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
light = 4
pin = 17
GPIO.setup(light, GPIO.OUT)
GPIO.setup(pin, GPIO.IN)

try:
    while 1:
        print(GPIO.input(pin))
        if not GPIO.input(pin):
            GPIO.output(light, True)
        else:
            GPIO.output(light, False)
        # GPIO.output(light, True)
except KeyboardInterrupt:
    print("ENd")
finally:
    GPIO.cleanup()
