import time
import spidev
import math

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device 0 (CE0)
spi.max_speed_hz = 500000

VREF = 3.2   # MCP3208 reference voltage

# MCP9700
OFFSET = 0.5 # 500 mV at 0°C
SCALE = 0.01 # 10 mV per °C

# Thermistor
R_FIXED = 10000  # 10kΩ fixed resistor
BETA = 3950      # Beta constant (ขึ้นกับชนิด Thermistor)
R0 = 10000       # Resistance at T0
T0 = 25 + 273.15 # Reference temperature in Kelvin

def read_adc(channel: int) -> int:
    """Read raw value from MCP3208 channel (0–7)."""
    if not 0 <= channel <= 7:
        raise ValueError("Channel must be 0–7")
    cmd = [0b00000110 | ((channel & 0x04) >> 2),
           (channel & 0x03) << 6,
           0]
    adc = spi.xfer2(cmd)
    return ((adc[1] & 0x0F) << 8) | adc[2]

def adc_to_voltage(adc_value: int) -> float:
    """Convert ADC value (0–4095) to voltage."""
    return (adc_value / 4095.0) * VREF

def voltage_to_temperature_mcp9700(voltage: float) -> float:
    """Convert voltage from MCP9700 to °C."""
    return (voltage - OFFSET) / SCALE

def voltage_to_temperature_thermistor(voltage: float) -> float:
    """Convert thermistor voltage divider output to °C."""
    if voltage <= 0 or voltage >= VREF:
        return None  # invalid reading
    R_therm = (voltage * R_FIXED) / (VREF - voltage)
    # Steinhart-Hart (Beta approximation)
    T_kelvin = 1 / (1/T0 + (1/BETA) * math.log(R_therm / R0))
    return T_kelvin - 273.15

try:
    while True:
        # MCP9700
        adc0 = read_adc(0)
        v0 = adc_to_voltage(adc0)
        t_mcp9700 = voltage_to_temperature_mcp9700(v0)

        # Thermistor
        adc1 = read_adc(1)
        v1 = adc_to_voltage(adc1)
        t_ntc = voltage_to_temperature_thermistor(v1)

        print(f"MCP9700: {t_mcp9700 - 2.0:.2f} °C (V={v0:.3f} V, ADC={adc0})")
        if t_ntc is not None:
            print(f"Thermistor: {t_ntc + 2.0:.2f} °C (V={v1:.3f} V, ADC={adc1})")
        else:
            print(f"Thermistor: Invalid reading (V={v1:.3f} V)")

        print("-" * 50)
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
