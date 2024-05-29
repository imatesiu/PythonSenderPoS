#!/usr/bin/python
import sys

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
import requests


ip = "192.168.0.133:8080"
urllabware = "http://"+ip+"/xonxoff_protocol.cgi"

def send(raw_data):
    x = requests.post(urllabware,  data=raw_data)
    print(x)
    
    

inter = "\n"

datar = "#K#R1/$100/(BENE \"A\")#T1#c"

data = datar.replace("#", inter+"#")

#dataf = data[4:]
print(data)
send(data)

#invio Chiusura Fiscale

datar = "#C3001"
data = datar.replace("#", inter+"#")
print(data)
send(data)
