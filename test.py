"""

   Pubsub envelope subscriber

   Author: Antonio Fontoura

"""
import zmq,json, struct, threading
from ledring_control import LedRingControl
from pvcommon.dataloggers import LoggerFactory
import time

test_input = [[1000,1046,112,16],
[2000,2035,222,33],
[3000,3004,344,50],
[4000,3964,461,67],
[5000,4982,570,85],
[6000,6000,685,103],
[7000,7008,805,121],
[8000,7968,923,139],
[9000,8985,1032,157],
[10000,9926,1141,174],
[11000,10924,1248,192],
[12000,11884,1356,210],
[13000,12883,1479,229],
[14000,13862,1579,247],
[15000,14899,1928,262],
[16000,15974,2504,273],
[17000,16896,3012,283],
[18000,17856,3511,293],
[19000,18816,4014,303],
[20000,19891,4552,314],
[21000,20928,5114,325],
[22000,21888,5610,335],
[23000,22848,6111,345],
[24000,23808,6609,355],
[25000,24921,7181,367]]
# [30000,30259,9674,415],
# [35000,34905,12071,465],
# [40000,40089,14396,517],
# [45000,45158,15843,543],
# [50000,50342,16349,585],
# [55000,55257,16854,625],
# [60000,60288,17392,666],
# [65000,65011,17712,706],
# [70000,70233,18500,745]]
# [32000,31987,15511,1312],



def set_ledring_brt(ledring, brt):

    shutdown_leds(ledring)
    if brt > 255*3:
        brt = 255*3

    leds = int(brt / 256)
    brt = int(brt % 256)    

    if leds > 0:
        r = 255
        if leds > 1:
            g = 255
            b = brt
        else:
            g = brt
            b = 0
    else:
        r = brt
        g = 0
        b = 0

    # print (f'{r} {g} {b}')

    try:
        for i in range(0,12):
            # print (f'{i} - {r} {g} {b}')
            ledring.set_led(i,[r,g,b])
    except Exception as ex:
        pass







def shutdown_leds(ledring):
    try:
        for i in range (0,12):
            ledring.set_led(i,[0,0,0])
    except Exception as ex:
        pass

wb_als = 0
def update_wb_als():
    global wb_als
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)


    subscriber.connect("tcp://10.10.20.48:5558")

    service_subscribed = "get_"
    subscriber.setsockopt(zmq.SUBSCRIBE, service_subscribed.encode('utf-8'))

    while True:
        [address, contents] = subscriber.recv_multipart()
        # print(f'a: {address}, c: {contents}')
        wb_als = int(json.loads(contents.decode('utf8'))["value"])

feedback_als = 0
def update_feedback_als(ledring):
    global feedback_als
    config = [{"ip": "10.10.20.48", 
            "data base": "wallbox_data", 
            "db user": "pvuser",
            "db password": "evboxpvsetup",
            "type": "influx-db"}]
    dblog = LoggerFactory.get_logger(config, request_type="influx-db")[0]
    
   
    while True:
        try:
            feedback_als = ledring.read_sensor()["als"]
            dblog.logCustomData("feedback_ledring",
        f'type="als" value={feedback_als}')
        except:
            pass
        
        time.sleep(0.1)

def margin(setpoint):
    if setpoint < 8000:
        return setpoint-50, setpoint+50
    else:
        return setpoint*0.99, setpoint*1.01

def main():
    """ main method """
    global wb_als
    global feedback_als
    ledring = LedRingControl("10.10.21.176")
    feedback_ledring = LedRingControl("10.10.21.149")
    ledring.connect()
    feedback_ledring.connect()
    

    shutdown_leds(feedback_ledring)

    # start continuous status update
    thread = threading.Thread(
        target=update_wb_als,
        daemon=True)
    thread.start()

    # start continuous status update
    thread2 = threading.Thread(
        target=update_feedback_als,
        args=(feedback_ledring, ),
        daemon=True)
    thread2.start()

    # time.sleep(2)
    # print(feedback_als)
    # print(wb_als)
    
    # set_ledring_brt(ledring,255*3)
    # print("feedback led ring")
    # set_ledring_brt(feedback_ledring,255*3)
    # time.sleep(5)
    # print(feedback_als)
    # print(wb_als)
    # shutdown_leds(ledring)
    # shutdown_leds(feedback_ledring)

    # exit()

  
  
    test_result = []
    try:

      

        setpoint = 1000
        i = 0
        brt = 0
        r = 0
        g = 0
        b = 0
        # brt = 155
        for test_case in test_input:
            brt = test_case[3]
            setpoint = test_case[0]

            if setpoint > 40000:
                set_ledring_brt(feedback_ledring,255*3)
            else:
                shutdown_leds(feedback_ledring)


            
            ledring_setpoint = test_case[2]
            
            print(f'try {setpoint}|{ledring_setpoint}:  {brt}')
            # ledring.set_all_leds(brt,[r,g,b])
            set_ledring_brt(ledring,brt)

            time.sleep(2)

            ledring_als = ledring.read_sensor()["als"]
            # feedback_ledring_als = feedback_ledring.read_sensor()["als"]
    


            test_setpoint = ledring_setpoint
            test_sensor = feedback_als

            # test_setpoint = setpoint
            # test_sensor = wb_als

            
            low_margin, high_margin = margin(test_setpoint)


            retries = 40
            
            while retries>0 and not (low_margin < test_sensor < high_margin):
                
                retries -= 1
                if test_sensor < test_setpoint:        
                    if (test_setpoint - test_sensor) > 100:
                        brt += int((test_setpoint - test_sensor)/100)
                    else:
                        brt += 1
                else:       
                    if (test_sensor-test_setpoint) > 100:
                        brt -= int((test_sensor - test_setpoint)/50)
                    else:
                        brt -= 1         
                    
                    if brt < 0:
                        brt = 0
                print(f'try {setpoint}|{ledring_setpoint}: {wb_als},{feedback_als}, {brt}')
                # ledring.set_all_leds(brt,[r,g,b])
                set_ledring_brt(ledring,brt)
                time.sleep(2)
                ledring_als = ledring.read_sensor()["als"]

                

                # feedback_ledring_als = feedback_ledring.read_sensor()["als"]
                test_sensor = feedback_als
                # test_sensor = wb_als
                
            
            if retries == 0:
                print(f'{setpoint} failed')

            ledring_als = ledring.read_sensor()["als"]
            # feedback_ledring_als = feedback_ledring.read_sensor()["als"]
            
            
            print(f'[{setpoint},{wb_als},{feedback_als},{brt}],')
            test_result.append([setpoint,wb_als,feedback_als,brt])
            shutdown_leds(ledring)
            # print(f'[{setpoint},{wb_als},{ledring_als},{brt},{r},{g},{b}]')
            time.sleep(2)
            setpoint += 6000
            i += 1
            



        

    finally:        
        shutdown_leds(ledring)
        shutdown_leds(feedback_ledring)

        for result in test_result:
            print(f'[{result[0]},{result[1]},{result[2]},{result[3]}],')
        print()

        for result in test_result:
            print(f'{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}')
        print()

        print("[",end="")
        for result in test_result:
            print(f'{result[1]}',end=",")
        print("]")



if __name__ == "__main__":

    main()