import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
device_address = 0x51
VCNL4200_DeviceID_REG = 0x0E

def sensor_exists():
    read = bus.read_word_data(device_address,0x0E)
    print(read)
    if read==0x1058:
        return true
	else:
	return false

try:
    print("\nSensor is initializing.")
    if (sensor_exists()):
        print("VCNL4200 found")
		#sensor_initialize()
		#print("VCNL4200 initialized")

finally:
    print("\nSensor is terminating.")

