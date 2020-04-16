import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
SENSOR_ADDR = 0x51
def setup():

  #Write to PS_CONF1 and PS_CONF2 to set Proximity Sensor (PS) settings.
  bus.write_word_data(SENSOR_ADDR, 0x3, 0B0001101000001000)
 
  #Write to ALS_CONF to turn Ambient Light Sensor (ALS) off.
  bus.write_word_data(SENSOR_ADDR, 0x0, 0B0100000100000000)
 
  #Write to PS_THDL_L and PS_THDL_H to set Proxmitt Sensor (PS) Threshhold.
  bus.write_word_data(SENSOR_ADDR, 0x6, 0B0001000000000000)  
 
  #Write to PS_CONF3 and PS_MS to set Proximity Sensor (PS) settings.
  bus.write_word_data(SENSOR_ADDR, 0x4, 0B0111000000000111)

# main code for operation

# Returns a list of byte values (integers between 0 and 255).
def read_sensor():
    bus.write_byte(SENSOR_ADDR, 0x8)
    read1 = bus.read_byte(SENSOR_ADDR)
    read2 = bus.read_byte(SENSOR_ADDR)    
    print(read1)
    print(read2)
    return read1

try:
    setup()
    print("\nSensor is initializing.")
    choice = ''
    while choice != 'q':
        data=read_sensor()
        #int value = int(data[1])*256 + int(data[0]); //Combines bytes
        time.sleep(0.1)
finally:
    print("\nLed Ring is terminating.")

