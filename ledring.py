import smbus
import RPi.GPIO as GPIO
import time

class LedRingLED:
    def __init__(self):
        super().__init__()
        self._bus = smbus.SMBus(1)
        self._device_address1 = 0x28
        self._device_address2 = 0x29
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)



    def shutdown(self):
        "Set Enable to Low to enter SHUTDOWN mode"
        GPIO.output(17, 0)
        return 

    def initialize(self):
        "Set Enable to High to enter INITIALIZATION"
        GPIO.output(17, 1)
        time.sleep(0.1)
        self._mode_select_normal()
        time.sleep(0.1)
        self._device_config1(1,1,1,1,0,0)
        time.sleep(0.1)
        return    

    def Mode_Select_Standby(self):
        "Set Chip_EN=0 to enter STANDBY mode"
        self._bus.write_byte_data(self._device_address1, 0x00, 0x00)
        self._bus.write_byte_data(self._device_address2, 0x00, 0x00)
        return

    def _mode_select_normal(self):
        "Set Chip_EN=1 to enter NORMAL mode"
        self._bus.write_byte_data(self._device_address1, 0x00, 0x40)
        self._bus.write_byte_data(self._device_address2, 0x00, 0x40)
        return
        
    #Device Configure
    def device_config1(self, Log_Scale_EN, Power_Save_EN, Auto_Incr_EN, PWM_Dithering_EN, Max_Current_Option, LED_Global_Off):
        config1=Log_Scale_EN*32+Power_Save_EN*16+Auto_Incr_EN*8+PWM_Dithering_EN*4+Max_Current_Option*2+LED_Global_Off
        self._bus.write_byte_data(self._device_address1, 0x01, config1)
        self._bus.write_byte_data(self._device_address2, 0x01, config1)
        return

    #Bank Select
    def LED_CONFIG0(self, LED7_Bank_EN, LED6_Bank_EN, LED5_Bank_EN, LED4_Bank_EN, LED3_Bank_EN, LED2_Bank_EN, LED1_Bank_EN, LED0_Bank_EN):
        config0=LED7_Bank_EN*128+LED6_Bank_EN*64+LED5_Bank_EN*32+LED4_Bank_EN*16+LED3_Bank_EN*8+LED2_Bank_EN*4+LED1_Bank_EN*2+LED0_Bank_EN
        self._bus.write_byte_data(self._device_address1, 0x02, config0)
        self._bus.write_byte_data(self._device_address2, 0x02, config0)
        return

    def Bank_Brightness_Set(self, BANK_BRIGHTNESS):
        self._bus.write_byte_data(self._device_address1, 0x03, BANK_BRIGHTNESS)
        self._bus.write_byte_data(self._device_address2, 0x03, BANK_BRIGHTNESS)
        return

    def Bank_Brightness_Set_U1(self, BANK_BRIGHTNESS):
        self._bus.write_byte_data(self._device_address1, 0x03, BANK_BRIGHTNESS)
        return

    def Bank_Brightness_Set_U2(self, BANK_BRIGHTNESS):
        self._bus.write_byte_data(self._device_address2, 0x03, BANK_BRIGHTNESS)
        return

    def Bank_Color_Set(self, BANK_A_COLOR, BANK_B_COLOR, BANK_C_COLOR):
        self._bus.write_byte_data(self._device_address1, 0x04, BANK_A_COLOR) #Set Bank Red Color Gray
        self._bus.write_byte_data(self._device_address1, 0x05, BANK_B_COLOR) #Set Bank Green Color Gray    
        self._bus.write_byte_data(self._device_address1, 0x06, BANK_C_COLOR) #Set Bank Blue Color Gray
        self._bus.write_byte_data(self._device_address2, 0x04, BANK_A_COLOR) #Set Bank Red Color Gray
        self._bus.write_byte_data(self._device_address2, 0x05, BANK_B_COLOR) #Set Bank Green Color Gray    
        self._bus.write_byte_data(self._device_address2, 0x06, BANK_C_COLOR) #Set Bank Blue Color Gray  
        return

    def LED_Brightness_Set(self, LED_Number, LED_Brightness):
        if(LED_Number<8):
            self._bus.write_byte_data(self._device_address1, LED_Number+0x07, LED_Brightness)
        else:
            self._bus.write_byte_data(self._device_address2, LED_Number+0x07, LED_Brightness)
        return

    def LED_color_set(self, LED_Number, GS_Red, GS_Green, GS_Blue):
        if(LED_Number<6):
            self._bus.write_byte_data(self._device_address1, LED_Number*3+0x0F, GS_Red)
            self._bus.write_byte_data(self._device_address1, LED_Number*3+0x10, GS_Green)
            self._bus.write_byte_data(self._device_address1, LED_Number*3+0x11, GS_Blue)     
        else:
            self._bus.write_byte_data(self._device_address2, (LED_Number-6)*3+0x0F, GS_Red)
            self._bus.write_byte_data(self._device_address2, (LED_Number-6)*3+0x010, GS_Green)
            self._bus.write_byte_data(self._device_address2, (LED_Number-6)*3+0x011, GS_Blue)
        return
            
    def Reset(self):
        self._bus.write_byte_data(self._device_address1, 0x27, 0xFF)
        self._bus.write_byte_data(self._device_address2, 0x27, 0xFF)
        return

    def set_all_leds(self, color = [0xff,0xff,0xff]):
        for i in range (0,11):
            self.LED_color_set(i,color[0], color[1], color[2])

    def chasing_effect_custom(self):
        for i in range (0,11):
            self.LED_color_set(i%12,0,0,30)
            self.LED_color_set((i+1)%12,0,0,45)
            self.LED_color_set((i+2)%12,0,0,60)
            self.LED_color_set((i+3)%12,0,0,90)
            self.LED_color_set((i+4)%12,0,0,150)
            self.LED_color_set((i+5)%12,0,0,200)
            self.LED_color_set((i+6)%12,0,0,255)
            self.LED_color_set((i+7)%12,0,0,200)
            self.LED_color_set((i+8)%12,0,0,150)
            self.LED_color_set((i+9)%12,0,0,900)
            self.LED_color_set((i+10)%12,0,0,60)
            self.LED_color_set((i+11)%12,0,0,45)
            time.sleep(0.1)
        return



def main():
    # main code for operation
    ledring = LedRingLED()
    try:        
        ledring.initialize()
        print("\nLed Ring is initializing.")
        choice = ''
        while choice != 'q':
            ledring.chasing_effect_custom()
    finally:
        print("\nLed Ring is terminating.")
        ledring.shutdown()

if __name__ == "__main__":
	main()
