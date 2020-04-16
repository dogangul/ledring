import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
device_address = 0x51



def set_ALS_CONF(val):
   bus.write_word_data(device_address,0x00,val)

def set_PS_CONF1_CONF2(val):
   bus.write_word_data(device_address,0x03,val)

def set_PS_CONF3_MS(val):
   bus.write_word_data(device_address,0x04,val)  

def set_PS_THDL_REG(val):
   bus.write_word_data(device_address,0x06,val)

def set_PS_THDH_REG(val):
   bus.write_word_data(device_address,0x07,val)  

def sensor_exists():
   return (bus.read_word_data(device_address,0x0E) == 0x1058)

def getProximity():
   return (bus.read_word_data(device_address,0x08))

def getAmbient():
   return (bus.read_word_data(device_address,0x09))

def initialize():
   #Edit the binary settings here to change default startup options
   set_ALS_CONF(0B01000000)
   set_PS_CONF1_CONF2(0B0000101100101010)
   set_PS_CONF3_MS(0B0000011101110000)

   #Set the PS interrupt levels
   set_PS_THDL_REG(0B0001001110001000)
   set_PS_THDH_REG(0B0010111011100000)

try:
   print("\nI2C is initializing.")
   if (sensor_exists()):
      print("VCNL4200 found")
   initialize()
   print("VCNL4200 initialized")
   choice = ''
   while choice != 'q':
      print("Proximity: ", getProximity())
      print("Ambient: ", getAmbient())

finally:
    print("Program is terminating")

