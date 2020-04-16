import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
device_address = 0x28
device_address1 = 0x28
device_address2 = 0x29
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)


def Shutdown():
   "Set Enable to Low to enter SHUTDOWN mode"
   GPIO.output(17, 0)
   return 

def Initialization():
   "Set Enable to High to enter INITIALIZATION"
   GPIO.output(17, 1)
   time.sleep(0.1)
   Mode_Select_Normal()
   time.sleep(0.1)
   Device_Config1(1,1,1,1,0,0)
   time.sleep(0.1)
   return    

def Mode_Select_Standby():
    "Set Chip_EN=0 to enter STANDBY mode"
    bus.write_byte_data(device_address1, 0x00, 0x00)
    bus.write_byte_data(device_address2, 0x00, 0x00)
    return

def Mode_Select_Normal():
    "Set Chip_EN=1 to enter NORMAL mode"
    bus.write_byte_data(device_address1, 0x00, 0x40)
    bus.write_byte_data(device_address2, 0x00, 0x40)
    return
    
#Device Configure
def Device_Config1(Log_Scale_EN, Power_Save_EN, Auto_Incr_EN, PWM_Dithering_EN, Max_Current_Option, LED_Global_Off):
    config1=Log_Scale_EN*32+Power_Save_EN*16+Auto_Incr_EN*8+PWM_Dithering_EN*4+Max_Current_Option*2+LED_Global_Off
    bus.write_byte_data(device_address1, 0x01, config1)
    bus.write_byte_data(device_address2, 0x01, config1)
    return

#Bank Select
def LED_CONFIG0(LED7_Bank_EN, LED6_Bank_EN, LED5_Bank_EN, LED4_Bank_EN, LED3_Bank_EN, LED2_Bank_EN, LED1_Bank_EN, LED0_Bank_EN):
    config0=LED7_Bank_EN*128+LED6_Bank_EN*64+LED5_Bank_EN*32+LED4_Bank_EN*16+LED3_Bank_EN*8+LED2_Bank_EN*4+LED1_Bank_EN*2+LED0_Bank_EN
    bus.write_byte_data(device_address1, 0x02, config0)
    bus.write_byte_data(device_address2, 0x02, config0)
    return

def Bank_Brightness_Set(BANK_BRIGHTNESS):
    bus.write_byte_data(device_address, 0x03, BANK_BRIGHTNESS)
    return

def Bank_Brightness_Set_U1(BANK_BRIGHTNESS):
    bus.write_byte_data(device_address1, 0x03, BANK_BRIGHTNESS)
    return

def Bank_Brightness_Set_U2(BANK_BRIGHTNESS):
    bus.write_byte_data(device_address2, 0x03, BANK_BRIGHTNESS)
    return

def Bank_Color_Set(BANK_A_COLOR, BANK_B_COLOR, BANK_C_COLOR):
    bus.write_byte_data(device_address1, 0x04, BANK_A_COLOR) #Set Bank Red Color Gray
    bus.write_byte_data(device_address1, 0x05, BANK_B_COLOR) #Set Bank Green Color Gray    
    bus.write_byte_data(device_address1, 0x06, BANK_C_COLOR) #Set Bank Blue Color Gray
    bus.write_byte_data(device_address2, 0x04, BANK_A_COLOR) #Set Bank Red Color Gray
    bus.write_byte_data(device_address2, 0x05, BANK_B_COLOR) #Set Bank Green Color Gray    
    bus.write_byte_data(device_address2, 0x06, BANK_C_COLOR) #Set Bank Blue Color Gray  
    return

def LED_Brightness_Set(LED_Number, LED_Brightness):
    if(LED_Number<8):
        bus.write_byte_data(device_address1, LED_Number+0x07, LED_Brightness)
    else:
        bus.write_byte_data(device_address2, LED_Number8+0x07, LED_Brightness)
    return

def LED_Color_Set(LED_Number, GS_Red, GS_Green, GS_Blue):
    if(LED_Number<6):
        bus.write_byte_data(device_address1, LED_Number*3+0x0F, GS_Red)
        bus.write_byte_data(device_address1, LED_Number*3+0x10, GS_Green)
        bus.write_byte_data(device_address1, LED_Number*3+0x11, GS_Blue)     
    else:
        bus.write_byte_data(device_address2, (LED_Number-6)*3+0x0F, GS_Red)
        bus.write_byte_data(device_address2, (LED_Number-6)*3+0x010, GS_Green)
        bus.write_byte_data(device_address2, (LED_Number-6)*3+0x011, GS_Blue)
    return
        
def Reset():
    bus.write_byte_data(device_address, 0x27, 0xFF)
    return

def breath_fresh_Red():
    Mode_Select_Normal()
    Device_Config1(1,1,1,1,0,0)
    LED_CONFIG0(1,1,1,1,1,1,1,1)#Bank control set, every LED in BANK
    Bank_Brightness_Set(0)
    Bank_Color_Set(255,0,0)#Bank color R:255 G:0 B:0
    for i in range (0,255):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    for i in range (255,0):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    return
        
def breath_fresh_Green():
    Mode_Select_Normal();
    Device_Config1(1,1,1,1,0,0)
    LED_CONFIG0(1,1,1,1,1,1,1,1)#Bank control set, every LED in BANK
    Bank_Brightness_Set(0);
    Bank_Color_Set(0,255,0)#Bank color R:0 G:255 B:0
    for i in range (0,255):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    for i in range (255,0):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    return

def breath_fresh_Blue():
    Mode_Select_Normal();
    Device_Config1(1,1,1,1,0,0)
    LED_CONFIG0(1,1,1,1,1,1,1,1)#Bank control set, every LED in BANK
    Bank_Brightness_Set(0)
    Bank_Color_Set(0,0,255)#Bank color R:200 G:0 B:0
    for i in range (0,255):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    for i in range (255,0):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    return

def breath_fresh_Yellow():
    Mode_Select_Normal();
    Device_Config1(1,1,1,1,0,0)
    LED_CONFIG0(1,1,1,1,1,1,1,1)#Bank control set, every LED in BANK
    Bank_Brightness_Set(0)
    Bank_Color_Set(255,255,0);#Bank color R:255 G:255 B:0
    for i in range (0,255):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    for i in range (255,0):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    return
        
def breath_fresh_Pink():
    Mode_Select_Normal();
    Device_Config1(1,1,1,1,0,0)
    LED_CONFIG0(1,1,1,1,1,1,1,1)#Bank control set, every LED in BANK
    Bank_Brightness_Set(0)
    Bank_Color_Set(255,0,255);#Bank color R:255 G:0 B:255
    for i in range (0,255):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    for i in range (255,0):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    return
        
def breath_fresh_Teal():
    Mode_Select_Normal();
    Device_Config1(1,1,1,1,0,0)
    LED_CONFIG0(1,1,1,1,1,1,1,1)#Bank control set, every LED in BANK
    Bank_Brightness_Set(0)
    Bank_Color_Set(200,0,0);#Bank color R:200 G:0 B:0
    for i in range (0,255):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    for i in range (255,0):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    return

def breath_fresh_White():
    Mode_Select_Normal();
    Device_Config1(1,1,1,1,0,0)
    LED_CONFIG0(1,1,1,1,1,1,1,1)#Bank control set, every LED in BANK
    Bank_Brightness_Set(0)
    Bank_Color_Set(255,255,255);#Bank color R:255 G:255 B:255
    for i in range (0,255):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    for i in range (255,0):
        Bank_Brightness_Set_U1(i)
        Bank_Brightness_Set_U2(i)
        time.sleep(0.005)
    return

def ChasingEffectFade_Red():
    Mode_Select_Normal()
    Device_Config1(1,1,1,1,0,0)
    for i in range (0,11):
        LED_Color_Set((i+0)%11,6*(i%11),0,0)
        LED_Color_Set((i+1)%11,8*(i%11),0,0)
        LED_Color_Set((i+2)%11,10*(i%11),0,0)
        LED_Color_Set((i+3)%11,12*(i%11),0,0)
        LED_Color_Set((i+4)%11,0*(i%11),0,0)
        LED_Color_Set((i+5)%11,0*(i%11),0,0)
        LED_Color_Set((i+6)%11,6*(i%11),0,0)
        LED_Color_Set((i+7)%11,8*(i%11),0,0)
        LED_Color_Set((i+8)%11,10*(i%11),0,0)
        LED_Color_Set((i+9)%11,12*(i%11),0,0)
        LED_Color_Set((i+10)%11,0*(i%11),0,0)
        LED_Color_Set((i+11)%11,0*(i%11),0,0)
        time.sleep(0.32)       
    for i in range (11,0):
        LED_Color_Set((i+0)%11,6*(i%11),0,0)
        LED_Color_Set((i+1)%11,8*(i%11),0,0)
        LED_Color_Set((i+2)%11,10*(i%11),0,0)
        LED_Color_Set((i+3)%11,12*(i%11),0,0)
        LED_Color_Set((i+4)%11,0*(i%11),0,0)
        LED_Color_Set((i+5)%11,0*(i%11),0,0)
        LED_Color_Set((i+6)%11,6*(i%11),0,0)
        LED_Color_Set((i+7)%11,8*(i%11),0,0)
        LED_Color_Set((i+8)%11,10*(i%11),0,0)
        LED_Color_Set((i+9)%11,12*(i%11),0,0)
        LED_Color_Set((i+10)%11,0*(i%11),0,0)
        LED_Color_Set((i+11)%11,0*(i%11),0,0)
        time.sleep(0.32) 
    return

def ChasingEffect_Custom():
    for i in range (0,11):
        LED_Color_Set(i%12,0,0,30)
        LED_Color_Set((i+1)%12,0,0,60)
        LED_Color_Set((i+2)%12,0,0,90)
        LED_Color_Set((i+3)%12,0,0,120)
        LED_Color_Set((i+4)%12,0,0,150)
        LED_Color_Set((i+5)%12,0,0,180)
        LED_Color_Set((i+6)%12,0,0,210)
        LED_Color_Set((i+7)%12,0,0,180)
        LED_Color_Set((i+8)%12,0,0,150)
        LED_Color_Set((i+9)%12,0,0,120)
        LED_Color_Set((i+10)%12,0,0,90)
        LED_Color_Set((i+11)%12,0,0,60)
        time.sleep(0.1)
    return
try:
    Initialization()
    print("\nLed Ring is initializing.")
    choice = ''
    while choice != 'q':
        ChasingEffect_Custom()
finally:
    print("\nLed Ring is terminating.")
    Shutdown()
