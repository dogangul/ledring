from random import randint
import time
import zmq
import json
import threading
from sensor import LedRingSensor
from ledring import LedRingLED

class LedRingServer:

    def __init__(self, server_port=5575):
        self._context = zmq.Context(1)
        self._server = None
        self._connection_failed = False
        self._port = server_port        
        self._sensor_data = {
            "proximity": 0, 
            "als": 0, 
            }

        self._sensor = LedRingSensor(sensitivity=0.003)
        self._led_ring = LedRingLED()
        self._animation_run = False
        self._animation_status = "stopped"
        

        # start continuous status update
        self._thread = threading.Thread(
            target=self._update_sensor,
            daemon=True)
        self._thread.start()

        self._animation_run_thread = None
        
    def open(self):
        self._server = self._context.socket(zmq.REP)
        self._server.bind(f'tcp://*:{self._port}')

        if (self._sensor.sensor_exists()):
            print("VCNL4200 found")
        self._sensor.initialize()
        print("VCNL4200 initialized")

        self._led_ring.initialize()

        return True

    def send(self, request):
        self._server.send(request)
        return True

    def close(self):
        self._server.close()
        self._context.term()

    def received_data(self):        
        request = self._server.recv()
        return request

    def set_led(self, brightness):
        # relaycontrol.changeRelay(state)
        return True

    def _update_sensor(self):        

        while True:            
            try:
                self._sensor_data["proximity"] = self._sensor.proximity()
                self._sensor_data["als"] = self._sensor.ambient_light()  
            except Exception as ex:
                print(f'sensor read error: {ex}')
            


    def animation_mode(self, mode = "chasing_effect"):
        while self._animation_run:
            self._animation_status = "running"
            self._led_ring.chasing_effect_custom()

        self._animation_status = "stopped"


    def enable_animation(self):
        self._animation_run = True

    def disable_animation(self):
        self._animation_run = False

    def decode_client_id(self, data):
        request_data = {}
        return_data = {"status":"OK", "descritpion":""}
        try:
            data = json.loads(data)
            if "LED" == data["service"]:

                # stop animation and wait until it has fully stopped
                self.disable_animation()
                while self._animation_status != "stopped":
                    time.sleep(0.1)

                if "all" == data["mode"]:
                    brt = data["brightness"]
                    color = data["color"]
                    self._led_ring.set_all_leds(brt, color)
                elif "individual" == data["mode"]:
                    brt = data["brightness"]
                    color = data["color"]
                    led_num = data["led_number"]
                    
                    self._led_ring.LED_color_set(led_num,color[0],color[1],color[2])
                    self._led_ring.LED_brightness_set(led_num,brt)
                elif "chasing_effect" == data["mode"]:
                    # start continuous animation mode
                    self._animation_run_thread = threading.Thread(
                        target=self.animation_mode,
                        daemon=True)
                    self.enable_animation()
                    self._animation_run_thread.start()
                else:
                    return_data = {"status":"NOK", "descritpion":"invalid LED Mode"}            
            elif "sensor" == data["service"]:
                return_data = self._sensor_data

        except KeyError as ex:
            print (f'Unkown command: {ex}')
            return_data = {"status":"NOK", "descritpion":"Unknown Command"}
        except json.JSONDecodeError as ex:
            print (f'Wrong json structure: {ex}')
            return_data = {"status":"NOK", "descritpion":"Wrong json structure"}
        
        return request_data, return_data



try:
    server_interface = LedRingServer("5575")

    server_interface.open()

    while True:
        #get data from client
        data = server_interface.received_data() 
        request_data, return_data = server_interface.decode_client_id(data)

        #server send response to client
        return_data = json.dumps(return_data).encode()
        server_interface.send(return_data)  
finally:
    server_interface.close_connection()
