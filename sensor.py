import smbus
import RPi.GPIO as GPIO
import time

class LedRingSensor:
   def __init__(self, sensitivity = 0.003):
      super().__init__()
      self._bus = smbus.SMBus(1)
      self._device_address = 0x51
      self._sensitivity = sensitivity

   def set_ALS_CONF(self, val):
      self._bus.write_word_data(self._device_address,0x00,val)

   def set_PS_CONF1_CONF2(self, val):
      self._bus.write_word_data(self._device_address,0x03,val)

   def set_PS_CONF3_MS(self, val):
      self._bus.write_word_data(self._device_address,0x04,val)  

   def set_PS_THDL_REG(self, val):
      self._bus.write_word_data(self._device_address,0x06,val)

   def set_PS_THDH_REG(self, val):
      self._bus.write_word_data(self._device_address,0x07,val)  

   def sensor_exists(self):
      return (self._bus.read_word_data(self._device_address,0x0E) == 0x1058)

   def proximity(self):
      return (self._bus.read_word_data(self._device_address,0x08))

   def ambient_light(self):
      return (self._bus.read_word_data(self._device_address,0x09))

   def initialize():
      #Edit the binary settings here to change default startup options
      if 0.003 == self._sensitivity :
         self.set_ALS_CONF(0B11000000)
      elif 0.006 == self._sensitivity :
         self.set_ALS_CONF(0B10000000)
      elif 0.012 == self._sensitivity :
         self.set_ALS_CONF(0B01000000)
      elif 0.024 == self._sensitivity :
         self.set_ALS_CONF(0B00000000)
      else:
         self.set_ALS_CONF(0B00000000)

      self.set_PS_CONF1_CONF2(0B0000101100101010)
      self.set_PS_CONF3_MS(0B0000011101110000)

      #Set the PS interrupt levels
      self.set_PS_THDL_REG(0B0001001110001000)
      self.set_PS_THDH_REG(0B0010111011100000)



def main():
   sensor = LedRingSensor(sensitivity=0.024)

   try:
      print("\nI2C is initializing.")
      if (sensor.sensor_exists()):
         print("VCNL4200 found")
      sensor.initialize()
      print("VCNL4200 initialized")
      choice = ''
      while choice != 'q':
         print("Proximity: ", sensor.proximity(), "  Ambient: ", sensor.ambient_light())

   finally:
      print("Program is terminating")

if __name__ == "__main__":
	main()





