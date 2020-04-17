import smbus
import RPi.GPIO as GPIO
import time

bus = smbus.SMBus(1)
device_address1 = 0x28
device_address2 = 0x29
device_address = 0x51
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

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
    bus.write_byte_data(device_address1, 0x03, BANK_BRIGHTNESS)
    bus.write_byte_data(device_address2, 0x03, BANK_BRIGHTNESS)
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
        bus.write_byte_data(device_address2, LED_Number+0x07, LED_Brightness)
    return

def LED_Color_Set(LED_Number, GS_Red, GS_Green, GS_Blue):
    if(LED_Number<6):
        bus.write_byte_data(device_address1, LED_Number*3+0x0F, int(GS_Red))
        bus.write_byte_data(device_address1, LED_Number*3+0x10, int(GS_Green))
        bus.write_byte_data(device_address1, LED_Number*3+0x11, int(GS_Blue))     
    else:
        bus.write_byte_data(device_address2, (LED_Number-6)*3+0x0F, int(GS_Red))
        bus.write_byte_data(device_address2, (LED_Number-6)*3+0x010, int(GS_Green))
        bus.write_byte_data(device_address2, (LED_Number-6)*3+0x011, int(GS_Blue))
    return
        
def Reset():
    bus.write_byte_data(device_address1, 0x27, 0xFF)
    bus.write_byte_data(device_address2, 0x27, 0xFF)
    return

def ChasingEffect_Custom(prox,amb):
    if amb > 1000 :
        dim = 1
    else:
        dim = 0.01
        
    if prox>1500:    
        LED_Color_Set(0,240*dim,0,0)
        LED_Color_Set(1,240*dim,0,0)
        LED_Color_Set(2,240*dim,0,0)
        LED_Color_Set(3,240*dim,0,0)
        LED_Color_Set(4,240*dim,0,0)
        LED_Color_Set(5,240*dim,0,0)
        LED_Color_Set(6,240*dim,0,0)
        LED_Color_Set(7,240*dim,0,0)
        LED_Color_Set(8,240*dim,0,0)
        LED_Color_Set(9,240*dim,0,0)
        LED_Color_Set(10,240*dim,0,0)
        LED_Color_Set(11,240*dim,0,0) 
    elif prox>1000:
        LED_Color_Set(0,220*dim,0,0)
        LED_Color_Set(1,220*dim,0,0)
        LED_Color_Set(2,220*dim,0,0)
        LED_Color_Set(3,220*dim,0,0)
        LED_Color_Set(4,220*dim,0,0)
        LED_Color_Set(5,220*dim,0,0)
        LED_Color_Set(6,220*dim,0,0)
        LED_Color_Set(7,220*dim,0,0)
        LED_Color_Set(8,220*dim,0,0)
        LED_Color_Set(9,220*dim,0,0)
        LED_Color_Set(10,220*dim,0,0)
        LED_Color_Set(11,0,0,0)  
    elif prox>750:
        LED_Color_Set(0,200*dim,20*dim,0)
        LED_Color_Set(1,200*dim,20*dim,0)
        LED_Color_Set(2,200*dim,20*dim,0)
        LED_Color_Set(3,200*dim,20*dim,0)
        LED_Color_Set(4,200*dim,20*dim,0)
        LED_Color_Set(5,200*dim,20*dim,0)
        LED_Color_Set(6,200*dim,20*dim,0)
        LED_Color_Set(7,200*dim,20*dim,0)
        LED_Color_Set(8,200*dim,20*dim,0)
        LED_Color_Set(9,200*dim,20*dim,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>600:
        LED_Color_Set(0,180*dim,40*dim,0)
        LED_Color_Set(1,180*dim,40*dim,0)
        LED_Color_Set(2,180*dim,40*dim,0)
        LED_Color_Set(3,180*dim,40*dim,0)
        LED_Color_Set(4,180*dim,40*dim,0)
        LED_Color_Set(5,180*dim,40*dim,0)
        LED_Color_Set(6,180*dim,40*dim,0)
        LED_Color_Set(7,180*dim,40*dim,0)
        LED_Color_Set(8,180*dim,40*dim,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>500:
        LED_Color_Set(0,160*dim,60*dim,0)
        LED_Color_Set(1,160*dim,60*dim,0)
        LED_Color_Set(2,160*dim,60*dim,0)
        LED_Color_Set(3,160*dim,60*dim,0)
        LED_Color_Set(4,160*dim,60*dim,0)
        LED_Color_Set(5,160*dim,60*dim,0)
        LED_Color_Set(6,160*dim,60*dim,0)
        LED_Color_Set(7,160*dim,60*dim,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>420:
        LED_Color_Set(0,140*dim,80*dim,0)
        LED_Color_Set(1,140*dim,80*dim,0)
        LED_Color_Set(2,140*dim,80*dim,0)
        LED_Color_Set(3,140*dim,80*dim,0)
        LED_Color_Set(4,140*dim,80*dim,0)
        LED_Color_Set(5,140*dim,80*dim,0)
        LED_Color_Set(6,140*dim,80*dim,0)
        LED_Color_Set(7,0,0,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>360:
        LED_Color_Set(0,120*dim,100*dim,0)
        LED_Color_Set(1,120*dim,100*dim,0)
        LED_Color_Set(2,120*dim,100*dim,0)
        LED_Color_Set(3,120*dim,100*dim,0)
        LED_Color_Set(4,120*dim,100*dim,0)
        LED_Color_Set(5,120*dim,100*dim,0)
        LED_Color_Set(6,0,0,0)
        LED_Color_Set(7,0,0,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>300:
        LED_Color_Set(0,100*dim,120*dim,0)
        LED_Color_Set(1,100*dim,120*dim,0)
        LED_Color_Set(2,100*dim,120*dim,0)
        LED_Color_Set(3,100*dim,120*dim,0)
        LED_Color_Set(4,100*dim,120*dim,0)
        LED_Color_Set(5,0,0,0)
        LED_Color_Set(6,0,0,0)
        LED_Color_Set(7,0,0,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>250:
        LED_Color_Set(0,80*dim,140*dim,0)
        LED_Color_Set(1,80*dim,140*dim,0)
        LED_Color_Set(2,80*dim,140*dim,0)
        LED_Color_Set(3,80*dim,140*dim,0)
        LED_Color_Set(4,0,0,0)
        LED_Color_Set(5,0,0,0)
        LED_Color_Set(6,0,0,0)
        LED_Color_Set(7,0,0,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>210:
        LED_Color_Set(0,60*dim,160*dim,0)
        LED_Color_Set(1,60*dim,160*dim,0)
        LED_Color_Set(2,60*dim,160*dim,0)
        LED_Color_Set(3,0,0,0)
        LED_Color_Set(4,0,0,0)
        LED_Color_Set(5,0,0,0)
        LED_Color_Set(6,0,0,0)
        LED_Color_Set(7,0,0,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>180:
        LED_Color_Set(0,40*dim,180*dim,0)
        LED_Color_Set(1,40*dim,180*dim,0)
        LED_Color_Set(2,0,0,0)
        LED_Color_Set(3,0,0,0)
        LED_Color_Set(4,0,0,0)
        LED_Color_Set(5,0,0,0)
        LED_Color_Set(6,0,0,0)
        LED_Color_Set(7,0,0,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    elif prox>160:
        LED_Color_Set(0,20*dim,220*dim,0)
        LED_Color_Set(1,0,0,0)
        LED_Color_Set(2,0,0,0)
        LED_Color_Set(3,0,0,0)
        LED_Color_Set(4,0,0,0)
        LED_Color_Set(5,0,0,0)
        LED_Color_Set(6,0,0,0)
        LED_Color_Set(7,0,0,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)
    else:
        LED_Color_Set(0,0,0,0)
        LED_Color_Set(1,0,0,0)
        LED_Color_Set(2,0,0,0)
        LED_Color_Set(3,0,0,0)
        LED_Color_Set(4,0,0,0)
        LED_Color_Set(5,0,0,0)
        LED_Color_Set(6,0,0,0)
        LED_Color_Set(7,0,0,0)
        LED_Color_Set(8,0,0,0)
        LED_Color_Set(9,0,0,0)
        LED_Color_Set(10,0,0,0)
        LED_Color_Set(11,0,0,0)

# main code for operation
try:
    Initialization()
    print("\nLed Ring is initializing.")
    if (sensor_exists()):
        print("VCNL4200 found")
    initialize()
    print("VCNL4200 initialized")
    choice = ''
    while choice != 'q':
        ChasingEffect_Custom(getProximity(),getAmbient())
        print("Proximity: ", getProximity(), "  Ambient: ", getAmbient())
finally:
    print("\nLed Ring is terminating.")
    Shutdown()
