#!/usr/bin/env python

"""A simple python script template.
"""

import serial
from ponyframe import TinyFrame as TF
import os
import sys
import time


TYPE_SIMPLE = 0x21
TYPE_HELLO = 0x22

def fallback_listener(tf: TF.TinyFrame, frame):
    print("Fallback listener")
    print(frame)

def simple_listener(tf: TF.TinyFrame, frame):
    print("simple listener")
    print(frame)

def hello_listener(tf: TF.TinyFrame, frame):
    print("hello listener")
    print(frame)


def main(arguments):
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
    tf.add_type_listener(TYPE_HELLO, hello_listener)
    
    while 1:
        tf.send(TYPE_HELLO, b"Hi Central")
        line = ser.read(ser.in_waiting)   # read a '\n' terminated line
        tf.accept(line)
        time.sleep(1)
    
    ser.close()
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
