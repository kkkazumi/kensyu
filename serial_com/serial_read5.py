# -*- coding: utf-8 -*-
import serial
import socket
import sys
import threading
import binascii
import numpy

import sys

number_irs = 1

class Serial_read:
    def __init__(self, port, baud):
        # シリアル通信の設定(
        self.ser = serial.Serial(port, baud, timeout=1)

    def conbine_high_low(self, str_high,str_low):
        data_high=binascii.b2a_hex(str_high)
        int_high=int(data_high,16)
        high = (int_high << 8)

        data_low=binascii.b2a_hex(str_low)
        int_low=int(data_low,16)
        low = (int_low& 0xFF)

        read_val = (high << 8|low)
        int_val = int(read_val)
        if int_val > 0 and int_val < 80:
            return int_val

    def read_val(self):
        read_val = numpy.zeros(number_irs)
        while True:
            serial_data = self.ser.read()
            if serial_data == 'H':
                for ir_num in range(number_irs):
                    str_high = self.ser.read()
                    str_low = self.ser.read()
                    read_val[ir_num] = self.conbine_high_low(str_high,str_low)
                self.ser.flushInput()
                if read_val[0]!= None:
                    #print read_val
                    return read_val

if __name__ == '__main__':
    #ser_port = "/dev/ttyACM1"
    ser_baud = 19200

    argvs = sys.argv
    ser_port = argvs[1]

    serial_test = Serial_read(ser_port,ser_baud)
    while True:
        val = serial_test.read_val()
        print(val)

