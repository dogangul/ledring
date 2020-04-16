import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
SENSOR_ADDR = 0x51
def setup():

  #Write to PS_CONF1 and PS_CONF2 to set Proximity Sensor (PS) settings.
  bus.write_word_data(SENSOR_ADDR, 0x3, 0B00011010, 0B00001000)
 
  #Write to ALS_CONF to turn Ambient Light Sensor (ALS) off.
  bus.write_word_data(SENSOR_ADDR, 0x0, 0B01000001, 0B00000000)
 
  #Write to PS_THDL_L and PS_THDL_H to set Proxmitt Sensor (PS) Threshhold.
  bus.write_word_data(SENSOR_ADDR, 0x6, 0B00010000, 0B00000000)  
 
  #Write to PS_CONF3 and PS_MS to set Proximity Sensor (PS) settings.
  bus.write_word_data(SENSOR_ADDR, 0x4, 0B01110000, 0B00000111)

# main code for operation

# Returns a list of byte values (integers between 0 and 255).
  def read_sensor():
    write = i2c_msg.write(SENSOR_ADDR, 0x8)
    read = i2c_msg.read(SENSOR_ADDR, 2)
    bus.i2c_rdwr(write, read)
    return read

try:
    setup()
    print("\nSensor is initializing.")
    choice = ''
    while choice != 'q':
        data=read_sensor()
        #int value = int(data[1])*256 + int(data[0]); //Combines bytes
        print(data)
        time.sleep(0.1)
finally:
    print("\nLed Ring is terminating.")
    Shutdown()
