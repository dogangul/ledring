import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
device_address = 0x51
VCNL4200_DeviceID_REG = 0x0E

def sensor_exists():
    print(bus.read_word_data(device_address,0x0E))
    return (bus.read_word_data(device_address,0x0E) == 0x1058)
try:
    print("\nSensor is initializing.")
    if (sensor_exists()):
        print("VCNL4200 found")
		#sensor_initialize()
		#print("VCNL4200 initialized")

finally:
    print("\nSensor is terminating.")

