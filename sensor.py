import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
SENSOR_ADDR = 0x51
VCNL4200_DeviceID_REG = 0x0E

def sensor_exists():
    read = bus.process_call(SENSOR_ADDR,VCNL4200_DeviceID_REG,SENSOR_ADDR)
    print(read)
	#if ((lowByte == 0x58) && (highByte == 0x10)) {
	#	return true;
	#}
	#return false

try:
    print("\nSensor is initializing.")
	if (sensor_exists()) {
		print("VCNL4200 found")
		#sensor_initialize()
		#print("VCNL4200 initialized")
	}

finally:
    print("\nSensor is terminating.")

