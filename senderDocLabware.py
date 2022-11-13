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


ip = "146.48.84.159"
urllabware = "http://"+ip+"/xonxoff_protocol.cgi"

def send(raw_data):
    x = requests.post(urllabware,  data=raw_data)
    print(x)
    
    

inter = "/n/r"

datar = "#K#C1#R1/$100/(BENE \"A\")#Q2#\"/?L/$1/(FL011074)#T4#c"
datar = "#K"

data = datar.replace("#", inter+"#")

dataf = data[4:]
print(dataf)
#send(dataf)

	
