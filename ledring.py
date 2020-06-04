import smbus
import RPi.GPIO as GPIO
import time

def rotate_left(arr_input): 
    arr = arr_input.copy()
    temp = arr[0] 
    for i in range(len(arr)-1): 
        arr[i] = arr[i+1] 
    arr[len(arr)-1] = temp 
    return arr

def array_diff(v1,v2):
    r = v2.copy()
    for i in range(len(r)):
        r[i] -= v1[i] 
    return r

def array_add(v1,v2, copy = False):
    if copy:
        r = v2.copy()
    else:
        r = v1
    for i in range(len(r)):
        r[i] += v2[i] 
    return r

def array_div(v,value):
    for i in range(len(v)):
        v[i] /= value

def integer_array(v):
    for i in range(len(v)):
        v[i] = int(v[i])
    return v



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
    def _device_config1(self, Log_Scale_EN, Power_Save_EN, Auto_Incr_EN, PWM_Dithering_EN, Max_Current_Option, LED_Global_Off):
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

    def LED_brightness_set(self, LED_Number, LED_Brightness):
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

    def set_all_leds(self,  color = [0xff,0xff,0xff]):
        for i in range (0,12):
            self.LED_color_set(i,color[0], color[1], color[2])


    def chasing_effect_custom(self):
        
        # v = [30,45,60,90,150,200,255,200,150,90,60,45]
        # v = [15,30,45,60,75,200,255,200,75,60,45,30]
        # v = [15,25,35,45,55,200,255,200,55,45,35,25]
        v = [0,5,10,15,150,200,255,200,150,15,10,5]
        # v = [0,5,10,15,20,25,255,25,20,15,10,5]
        steps = 5

        v_led = v
        while True:
            v_new = rotate_left(v_led)
            v_diff = array_diff(v_led,v_new)
            array_div(v_diff,steps)

            for i in range(steps):
                array_add(v_led,v_diff)
                v_final = integer_array(v_led.copy())
                for x in range (0,12):
                    self.LED_color_set(x,0,0,v_final[x])
                   
           
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
