"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-keypad
"""


import RPi.GPIO as GPIO
import time
# Define keypad layout
KEYPAD = [
    [1, 2, 3, 'A'],
    [4, 5, 6, 'B'],
    [7, 8, 9, 'C'],
    ['*', 0, '#', 'D']
]

# Define GPIO pins for rows and columns
ROWS = [2, 3, 4,17]
COLS = [6, 13, 19, 26]
RED = 14 
GREEN = 15 
BLUE = 18 

colors = [
    (False, False, False),  # ขาว
    (False, False, True),   # เหลือง
    (False, True, False),   # ม่วง
    (False, True, True),    # แดง
    (True, False, False),   # ฟ้าอ่อน
    (True, False, True),    # เขียว
    (True, True, False),    # น้ำเงิน
]
# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
# Set up row pins as inputs with pull-up resistors
for row_pin in ROWS:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up column pins as outputs
for col_pin in COLS:
    GPIO.setup(col_pin, GPIO.OUT)
    GPIO.output(col_pin, GPIO.HIGH)

def get_key():

    for col_num, col_pin in enumerate(COLS):
        GPIO.output(col_pin, GPIO.LOW)

        for row_num, row_pin in enumerate(ROWS):
            if GPIO.input(row_pin) == GPIO.LOW:
                GPIO.output(col_pin, GPIO.HIGH)
                return KEYPAD[row_num][col_num]

        GPIO.output(col_pin, GPIO.HIGH)

    return None

try:
    while True:
        pressed_key = get_key()
        
        if pressed_key is not None and isinstance(pressed_key, int) and 1 <= pressed_key <= 7:
            print(f"Pressed: {pressed_key}")
            GPIO.output(RED, colors[pressed_key-1][0])
            GPIO.output(GREEN, colors[pressed_key-1][1])
            GPIO.output(BLUE, colors[pressed_key-1][2])
        else:
            GPIO.output(RED, True)
            GPIO.output(GREEN, True)
            GPIO.output(BLUE, True)

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
