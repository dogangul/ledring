import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
device_address = 0x51



def set_ALS_CONF(val):
    bus.write_word_data(device_address,0x00,val)

def sensor_exists():
    return (bus.read_word_data(device_address,0x0E) == 0x1058)

def initialize():
    set_ALS_CONF(0B01000000) #Edit the binary settings here to change default startup options

	#set_PS_CONF1_CONF2();
	#set_PS_CONF3_MS();

	#Set the PS interrupt levels
	#write16_LowHigh(VCNL4200_PS_THDL_REG, B10001000, B00010011);
	#write16_LowHigh(VCNL4200_PS_THDH_REG, B11100000, B00101110);

try:
    print("\nI2C is initializing.")
    if (sensor_exists()):
        print("VCNL4200 found")
    initialize()
    print(bus.read_word_data(device_address,0x00))
        # print("VCNL4200 initialized")

finally:
    print("\nSensor is terminating.")

