import time
import spidev
spi = spidev.SpiDev() # Open SPI bus
spi.open(0, 0)
def ReadChannel(channel): # read channel (0-7) from MCP3208
    adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
    #ส่งข้อมูลสาม byte แรก ตามที่ Datasheet ก าหนด แล้วรอรับค่าที่แปลงได้
    data = ((adc[1] & 15) << 8) + adc[2]
    #บิตสูง 4 บิตอยู่ในไบต์ที่สอง เลยใช้ AND (& 15) เพื่อเก็บเฉพาะ 4 บิตล่าง แล้วเลื่อนบิตซ้าย 8 ต าแหน่ง
    # เพื่อให้สามารถบวกกับ 8 บิตจากไบต์ที่สามได้พอดี
    return data
while True:
    reading = ReadChannel(0)
    voltage = reading * 3.3 / 4096
    print("Reading=%d\t Voltage=%f" % (reading, voltage))
    time.sleep(1)