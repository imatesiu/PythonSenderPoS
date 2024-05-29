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
import time
 
ip = "146.48.89.151:8080"
urllabware = "http://"+ip+"/xonxoff_protocol.cgi"
 
def send(raw_data):
    x = requests.post(urllabware,  data=raw_data)
    print(x)
    print(x.text)

import sys
print ('argument list', sys.argv)
name = sys.argv[1]
 
f = open(name, "r")

for n in range(2):
	send(f.read())
	print(n)

