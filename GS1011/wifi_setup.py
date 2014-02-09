__author__ = 'carledwards'

#
# for use with GS1011 evaluation kit
#

import serial
import threading
import sys
import signal
import time
from datetime import datetime
import StringIO

def signal_handler(signal, frame):
    print "closing serial port"
    ser.close()
    sys.exit(0)

debugFlag = False
ser = serial.Serial()
buf = ''

class CommandTimeoutError(Exception):
    def __init__(self, cmd, buf):
        self.cmd = cmd
        self.buf = buf
    def __str__(self):
        return "cmd: %s, buffer: %s" % (repr(self.cmd), repr(self.buf))

class GSUsageError(Exception):
    def __init__(self, cmd, buf):
        self.cmd = cmd
        self.buf = buf
    def __str__(self):
        return "cmd: %s, buffer: %s" % (repr(self.cmd), repr(self.buf))


def debug(msg):
    if debugFlag:
        print(msg)

def gs_read_serial():
    global buf
    while ser and ser.isOpen():
        c = ser.read(1)
        #sys.stdout.write(c)
        buf = ''.join([buf, c])

def gs_strip_result(text):
    lines = StringIO.StringIO(text).readlines()
    # skip the first 2 lines (an echo of the command)
    result = []
    for line in lines[2:-1]:
        line = line.replace('\n','').replace('\r','')
        if len(line) == 0:
            continue
        result.append(line)
    return result

def gs_send_command(cmd, expected_result='OK\r\n', log_expected_result=True, error_result='ERROR: ', timeout=2):
    global buf
    buf = '' # reset the buffer
    start = datetime.now()
    debug("executing command: %s" % cmd)
    ser.write(''.join([cmd, "\n"]))
    while True:
        if expected_result in buf:
            return gs_strip_result(buf)
        if error_result in buf:
            raise GSUsageError(cmd, buf)

        delta = datetime.now() - start
        elapsed = delta.seconds + (float(1) / delta.microseconds)
        if elapsed >= timeout:
            raise CommandTimeoutError(cmd, buf)

        # wait for buffer to fill
        time.sleep(.25)
        debug(buf)

def gs_get_version():
    return gs_send_command("AT+VER=?")

def gs_get_mac():
    return gs_send_command("AT+NMAC=?")

def gs_get_wireless_status():
    return gs_send_command("AT+WSTATUS")

def get_module_info():
    print "version: %s" % gs_get_version()
    print "mac address: %s" % gs_get_mac()
    print "version: %s" % gs_get_wireless_status()

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
    t = threading.Thread(target=gs_read_serial)
    t.daemon = True
    t.start()

    get_module_info()


    # wait for CTRL+C to stop
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print ("Unexpected error: %s" % e)
        exit(0)

