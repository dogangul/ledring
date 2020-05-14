"""

   Pubsub envelope subscriber

   Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""
import zmq,json, struct
from ledring_control import LedRingControl

def main():
    """ main method """

    # Prepare our context and publisher
    context    = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    subscriber.connect("tcp://10.10.20.48:5558")

    service_subscribed = "get_"
    subscriber.setsockopt(zmq.SUBSCRIBE, service_subscribed.encode('utf-8'))

    ledring = LedRingControl("10.10.21.176")
    

    while True:
         # Read envelope with address
         [address, contents] = subscriber.recv_multipart()

         print(f'a: {address}, c: {contents}')

    # # We never get here but clean up anyhow
    subscriber.close()
    context.term()

if __name__ == "__main__":
    main()