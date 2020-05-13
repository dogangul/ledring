"""
stuff for controlling the relays on the dut
via ssh
"""

import logging
import time, socket
import zmq
import json


logger = logging.getLogger(__name__)


class LedRingControl:

    SERVER_PORT = "5575"

    def __init__(self, ledring_ip, timeout_ms = 2500):
        self._ip = ledring_ip        
        self._server_endpoint = f'tcp://{self._ip}:{self.SERVER_PORT}'
        self._connection_failed = False
        self._context = zmq.Context(1)
        self._client = None
        self._timeout = timeout_ms

    def __del__(self):
        self.close_connection()
        self._context.term()        
        

    def connect(self):
        #TODO check for connection fail
        self._client = self._context.socket(zmq.REQ)
        self._client.connect(self._server_endpoint)
        return True

    def close_connection(self):
        self._client.setsockopt(zmq.LINGER, 0)
        self._client.close()

    def _execute_command(self,data, retries=0):
        # Configure server polling
        poll = zmq.Poller()
        poll.register(self._client, zmq.POLLIN)

        retries_left = retries + 1

        while retries_left:
            retries_left -= 1
            request = json.dumps(data).encode()
            logger.debug(f"I: Sending {request}")
            self._client.send(request)
            
            socks = dict(poll.poll(self._timeout))
            if socks.get(self._client) == zmq.POLLIN:
                reply = self._client.recv()     
                logger.debug("I: Received")
                return reply

            elif 0 < retries_left:
                logger.debug("W: No response from server, retrying…")
                
                # Socket is confused. Close and remove it.
                self.close_connection()
                poll.unregister(self._client)
                
                logger.debug(f"I: Reconnecting and resending {request}")
                # Create new connection
                self.connect()
                poll.register(self._client, zmq.POLLIN)
                self._client.send(request) 
            else:
                self.close_connection()
                poll.unregister(self._client)
                self.connect()
                logger.debug("I: Timeout")

        raise Exception("Failure sending command: Did not get any response. Check the connection to the kit.")

    def set_all_leds(self, brightness=0, color=[0xff,0xff,0xff]):
        data = {"service":"LED"}
        
        data["brightness"] = brightness
        data["color"] = color
        data["mode"] = "all"
        reply = self._execute_command(data)
        if reply is None:
            return False
        else:
            return True

    def read_sensor(self):
        data = {"service": "sensor"}
        reply = self._execute_command(data)
        return json.loads(reply)

    
    def _reconnect(self):
        self.connect()


    def disconnect(self):
        self._client.close()

    def __del__(self):
        self.disconnect()
