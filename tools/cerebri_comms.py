#!/usr/bin/env python

"""A simple python script template.
"""

import serial
from ponyframe import TinyFrame as TF
from simple_pb2 import SimpleMessage
import sys
import time

TYPE_HELLO = 0x21
TYPE_SIMPLE = 0x22

value = 0

def fallback_listener(tf: TF.TinyFrame, frame: TF.TF_Msg):
    print("Fallback listener")
    print(frame)

def simple_listener(tf: TF.TinyFrame, frame: TF.TF_Msg):
    global value
    msg = SimpleMessage()
    msg.ParseFromString(frame.data)
    print('{:d}: {:d}'.format(msg.clock, msg.lucky_number))
    if value == msg.lucky_number:
        value+=1

def main(arguments):
    global value
    
    tf = TF.TinyFrame()
    tf.ID_BYTES=1
    tf.LEN_BYTES=2
    tf.TYPE_BYTES=1
    tf.CKSUM_TYPE = 'crc16'
    tf.USE_SOF_BYTE=True
    tf.SOF_BYTE = 0x01

    ser = serial.Serial('/dev/pts/3', 921600, timeout=10)
    tf.write = ser.write
    tf.add_fallback_listener(fallback_listener)
    tf.add_type_listener(TYPE_SIMPLE, simple_listener)

    ready = False
    start = time.time()

 
    while 1:
        # send message
        if ready:
            tf.send(type=TYPE_SIMPLE, pld=SimpleMessage(
                lucky_number=value, clock=int((time.time() - start)*1e3)
                ).SerializeToString())
        
        #tf.send(type=TYPE_HELLO, pld=b"hi")
        
        # read messages
        line = ser.read(ser.in_waiting)   # read a '\n' terminated line
        tf.accept(line)

        if len(line) > 0 and not ready:
            start = time.time()
            ready = True

        # sleep 0.01 seconds
        time.sleep(0.01)
    
    ser.close()
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
