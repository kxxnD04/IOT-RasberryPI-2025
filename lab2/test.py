import time
import spidev
import RPi.GPIO as GPIO

LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(LED_PIN, 10000)
pwm.start(0)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def read_adc_ch0():
    cmd = [0b00000110, 0b00000000, 0b00000000]
    adc = spi.xfer2(cmd)
    result = ((adc[1] & 0x0F) << 8) | adc[2]
    return result

def read_adc(channel):
    if not 0 <= channel <= 7:
        raise ValueError("Channel must be 0-7")

    cmd = [0b00000110 | ((channel & 0x04) >> 2),  # Start bit + MSB of channel
           (channel & 0x03) << 6,                 # Remaining 2 bits of channel
           0]
    adc = spi.xfer2(cmd)
    result = ((adc[1] & 0x0F) << 8) | adc[2]
    return result
def read_adc_avg(channel, samples=100):
    total = 0
    for _ in range(samples):
        total += read_adc(channel)
        time.sleep(0.001)
    return total // samples
try:
    while True:
        adc_value = read_adc_ch0()
        # adc_value = read_adc(5)
        print(adc_value)
        duty_cycle = (adc_value / 4095) * 100
        # print(duty_cycle)
        if adc_value < 100:
            pwm.ChangeDutyCycle(0)
        # elif adc_value >= 3700:
        #     adc_value = adc_value - 3095
        #     pwm.ChangeDutyCycle((adc_value / 1000) * 100)
        else:
            pwm.ChangeDutyCycle(duty_cycle)

        time.sleep(0.01)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    spi.close()