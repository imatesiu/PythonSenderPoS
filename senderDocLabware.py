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
 
ip = "146.48.89.12:8080"
urllabware = "http://"+ip+"/xonxoff_protocol.cgi"
 
def send(raw_data):
    x = requests.post(urllabware,  data=raw_data)
    print(x.text)

 
for x in range(1):
	inter = "\n"
	datar = "#K#R1/$100/(BENE \"A\")#\"/?L/$1/(FL011074)#T4/(Pag. Elettronico|dati canale operazione)#c"   
	data = datar.replace("#", inter+"#")
 
	dataf = data[4:]
	print(data)
	send(data)
 
	#time.sleep(2)
	#invio Chiusura Fiscale
 
	#datar = "#C3001"
	#datar = "#x"
	data = datar.replace("#", inter+"#")
	print(data)
	send(data)
 
	time.sleep(20)

