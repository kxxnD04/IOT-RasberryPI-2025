from RPLCD.i2c import CharLCD 
import time
 # สร้ำงออบเจ็กต์ LCD
import smbus3
bus = smbus3.SMBus(1)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A00',
              auto_linebreaks=True,
              backlight_enabled=True)

while 1:

    bus.i2c_wr(0x44,[0x2C,0x06])
    time.sleep(0.5)
    msg  = bus.i2c_rd(0x44, 6)
    data = bytes(msg)
    bus.close
    # Convert the data
    temp = data[0] * 256 + data[1]
    cTemp = -45 + (175 * temp / 65535.0)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    # Output data to screen
    print( "Temperature in Celsius is : %.2f C" %cTemp)

    print( "Relative Humidity is : %.2f %%RH" %humidity)
    lcd.clear() # ล้ำงหน้ำจอ  สดงข้อควำมใหม่
    lcd.write_string("Humid: " + f"{humidity:.2f}" + "%.")
    lcd.crlf()
    lcd.write_string("Temp: " + f"{cTemp:.2f}" + " C.")
    time.sleep(2)
