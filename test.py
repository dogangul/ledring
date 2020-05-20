"""

   Pubsub envelope subscriber

   Author: Antonio Fontoura

"""
import zmq,json, struct, threading
from ledring_control import LedRingControl
from pvcommon.dataloggers import LoggerFactory
import time

test_input = [[1000,1008,2172,180],
# [2000,2006,4871,412],
# [3000,2995,6330,535],
# [4000,3993,6850,577],
# test_input = [[5000,5001,7402,400],
# [6000,5990,7910,663],
# [7000,6998,8455,707],
# [8000,7987,8957,760],
# [9000,8985,9268,788],
# [10000,9964,9588,809],
# [11000,10944,9861,832],
# [12000,11942,10155,857],
# [13000,12960,10426,882],
# [14000,13939,10690,906],
# [15000,14937,10998,931],
# [16000,15936,11272,957],
# [17000,16972,11570,983],
# [18000,17971,11866,1010],
# [19000,18969,12145,1034],
# [20000,19929,12408,1055],
# [21000,20966,12656,1076],
# [22000,21964,12919,1097],
# [23000,22963,13182,1119],
# [24000,24000,13437,1143],
[25000,25036,11447,916],
# [26000,25958,13927,1188],
# [27000,26956,14196,1210],
# [28000,27955,14469,1233],
# [29000,28953,14702,1256],
# [30000,29990,14976,1279],
# [31000,30950,15218,1301],
# [32000,31948,15489,1321],
# [33000,32947,15730,1342],
# [34000,33984,15998,1364],
# [35000,34944,16267,1385],
# [36000,35980,16540,1407],
[37000,36940,14511,1162]]
# [32000,31987,15511,1312],



def set_ledring_brt(ledring, brt):

    shutdown_leds(ledring)
    if brt > 255*6:
        brt = 255*6

    leds = int(brt / 256)
    brt = int(brt % 256)
    for i in range(0,6):
        
        if i < leds:
            # print(f'{i} 255')
            ledring.set_led(i,[255,255,255])
            ledring.set_led(11-i,[255,255,255])
        elif i > leds:
            # print(f'{i} 0')
            ledring.set_led(i,[0,0,0])
            ledring.set_led(11-i,[0,0,0])
        else:
            # print(f'{i} {brt}')
            ledring.set_led(leds,[brt,brt,brt])
            ledring.set_led(11-leds,[brt,brt,brt])




def shutdown_leds(ledring):
    for i in range (0,12):
        ledring.set_led(i,[0,0,0])

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

    time.sleep(2)
    print(feedback_als)
    print(wb_als)
    set_ledring_brt(ledring,255*6)
    set_ledring_brt(feedback_ledring,255*6)
    time.sleep(2)
    print(feedback_als)
    print(wb_als)
    shutdown_leds(ledring)
    shutdown_leds(feedback_ledring)

    # exit()

  
  

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

            retries = 40
            
            while retries>0 and not ((test_setpoint-75) < test_sensor < (test_setpoint+75)):
                
                retries -= 1
                if test_sensor < test_setpoint:        
                    if (test_setpoint - test_sensor) > 100:
                        brt += int((test_setpoint - test_sensor)/50)
                    else:
                        brt += 1
                else:       
                    if (test_sensor-test_setpoint) > 100:
                        brt -= int((test_sensor - test_setpoint)/50)
                    else:
                        brt -= 1         
                    
                    if brt < 0:
                        brt = 0

                # ledring.set_all_leds(brt,[r,g,b])
                set_ledring_brt(ledring,brt)
                time.sleep(1)
                ledring_als = ledring.read_sensor()["als"]

                print(f'try {setpoint}|{ledring_setpoint}: {wb_als},{feedback_als}, {brt}')

                # feedback_ledring_als = feedback_ledring.read_sensor()["als"]
                test_sensor = feedback_als
                # test_sensor = wb_als
                
            
            if retries == 0:
                print(f'{setpoint} failed')

            ledring_als = ledring.read_sensor()["als"]
            # feedback_ledring_als = feedback_ledring.read_sensor()["als"]
            
            
            print(f'[{setpoint},{wb_als},{feedback_als},{brt}],')
            shutdown_leds(ledring)
            # print(f'[{setpoint},{wb_als},{ledring_als},{brt},{r},{g},{b}]')
            time.sleep(2)
            setpoint += 6000
            i += 1
            



        

        # while True:
        #      # Read envelope with address
        #      [address, contents] = subscriber.recv_multipart()

        #      print(f'a: {address}, c: {contents}')
        #      c = contents.decode('utf8')
        #      print(c)
        #      c2 = json.loads(c)
        #      print(c2["value"])        

        # # We never get here but clean up anyhow
        # subscriber.close()
        # context.term()
    finally:        
        shutdown_leds(ledring)
        shutdown_leds(feedback_ledring)


if __name__ == "__main__":

    main()