__author__ = 'carledwards'

#
# for use with GS1011 evaluation kit
#

import serial
import threading
import sys
import signal
import time

def signal_handler(signal, frame):
    print "closing serial port"
    ser.close()
    sys.exit(0)

ser = serial.Serial()

def read_serial():
    while ser and ser.isOpen():
        print ser.read(1),

def main():
    ser.port = '/dev/tty.usbserial-FTGDJL78'
    ser.baudrate = 9600
    print ser
    ser.open()
    if not ser.isOpen():
        print "serial port could not be opened"
        return
    print "serial port opened"

    # handle CTRL+C
    signal.signal(signal.SIGINT, signal_handler)

    # start our reading thread
    t = threading.Thread(target=read_serial)
    t.start()

    # get the version of the module
    ser.write("at+ver=?\n")

    # wait for CTRL+C to stop
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

