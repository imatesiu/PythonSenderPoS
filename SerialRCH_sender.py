#!/usr/bin/python
import sys
import urllib2, base64
import ssl
#import requests
import time
from base64 import b64encode
#from requests.auth import HTTPDigestAuth
#from requests.auth import HTTPBasicAuth
import hashlib
import re
import datetime
import json
import csv
import fileinput
import hmac
import hashlib
import base64
import time
from xml.dom import minidom

#from requests.packages.urllib3.exceptions import InsecureRequestWarning

#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/cu.usbmodem621',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS, timeout=1
)

#ser = serial.Serial('/dev/cu.usbmodem621',9600, timeout=1)
print "S1"
ser.isOpen()
print "S2"

while True:
    cmd = raw_input("Enter command or 'exit':")
        # for Python 2
    #cmd = input("Enter command or 'exit':")
        # for Python 3
    if cmd == 'exit':
        ser.close()
        exit()
    else:
    	print cmd
        ser.write(cmd.encode('HEX'))
        out = ser.read()
        print('Receiving...'+out)

ser.write('K') 
ser.write('C1 =R1/$200/(Reparto 01) =S')
ser.write('T1')
print "S3"

#line = ser.readline()

#print line
ser.close()  