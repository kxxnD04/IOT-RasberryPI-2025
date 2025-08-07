import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
RED = 14 # green
GREEN = 15 # yellow
BLUE = 18 # green
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

colors = [
    (False, False, False),  # ขาว
    (False, False, True),   # ฟ้า
    (False, True, False),   # เขียว
    (False, True, True),    # ฟ้าอ่อน
    (True, False, False),   # แดง
    (True, False, True),    # ม่วง
    (True, True, False),    # เหลือง
]

try:
    while 1:
        for color in colors:
            GPIO.output(RED, color[0])
            GPIO.output(GREEN, color[1])
            GPIO.output(BLUE, color[2])
            time.sleep(1)

except KeyboardInterrupt:
    print("ENd")
finally:
    GPIO.cleanup()
