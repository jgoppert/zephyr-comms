#!/usr/bin/env python3
import time
import asyncio
import serial_asyncio
from ponyframe import TinyFrame as TF
from simple_pb2 import SimpleMessage
import threading
from argparse import ArgumentParser


TYPE_HELLO = 0x21
TYPE_SIMPLE = 0x22


class SynapseProtocol(asyncio.Protocol):

    def __init__(self, on_con_lost):
        tf = TF.TinyFrame()
        tf.ID_BYTES=1
        tf.LEN_BYTES=2
        tf.TYPE_BYTES=1
        tf.CKSUM_TYPE = 'crc16'
        tf.USE_SOF_BYTE=True
        tf.SOF_BYTE = 0x01
        tf.add_fallback_listener(self.handle_fallback)
        tf.add_type_listener(TYPE_SIMPLE, self.handle_simple)
        self.tf = tf
        self.value = 0
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        self.transport = transport
        self.tf.write = transport.write
        self.start = time.time()
        print('port opened', transport)

    def data_received(self, data):
        self.tf.accept(data)

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()
        self.on_con_lost.set_result(True)

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')

    def handle_fallback(self, tf: TF.TinyFrame, frame: TF.TF_Msg):
        print("Fallback listener")
        print(frame)

    def handle_simple(self, tf: TF.TinyFrame, frame: TF.TF_Msg):
        msg = SimpleMessage()
        msg.ParseFromString(frame.data)
        print('{:d}: {:d}'.format(msg.clock, msg.lucky_number))
        if self.value == msg.lucky_number:
            self.value += 1


async def main():

    # parser
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_tcp = subparsers.add_parser('tcp', help='tcp connection')
    parser_tcp.add_argument('host', help='host')
    parser_tcp.add_argument('port', help='port')

    parser_serial = subparsers.add_parser('serial', help='serial connection')
    parser_serial.add_argument('device', help='device')
    parser_serial.add_argument('baud', help='baudrate')

    args = parser.parse_args()

    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()

    if args.command is None:
        print('syntax error')
        parser.print_usage()
        return
    elif args.command == 'tcp':
        transport, protocol = await loop.create_connection(
            lambda: SynapseProtocol(on_con_lost),
            args.host, int(args.port))
    elif args.command == 'serial':
        transport, protocol = await serial_asyncio.create_serial_connection(
            loop, lambda: SynapseProtocol(on_con_lost), args.device, baudrate=int(args.baud))
    else:
        print('unsupported command', args.command)
        parser.print_usage()
        return

    while True:
        await asyncio.sleep(1)
        protocol.tf.send(type=TYPE_SIMPLE, pld=SimpleMessage(
            lucky_number=protocol.value, clock=int((time.time() - protocol.start)*1e3)
            ).SerializeToString())

    try:
        await on_con_lost
    finally:
        transport.close()

asyncio.run(main())
