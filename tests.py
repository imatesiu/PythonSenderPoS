#!/usr/bin/python
#!/usr/bin/python
import sys
import urllib2, base64
import ssl
import requests
import time
from base64 import b64encode
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import datetime as date
import hashlib
import re
from datetime import datetime
import json
import csv
import fileinput
import hmac
import hashlib
import base64


user = "0001ab02"
password = "admin"
set_ip_server = "putsreq.com" #"10.10.56.136"
matricola = "53SNS3000011"
url = "HiuNgoNkN7NXF27hE0z4"

def send_post(content, url):
	print content, url
	response = requests.post('https://'+set_ip_server+'/'+url,data=content,auth=HTTPBasicAuth(user, password),headers={"Content-Type": "application/x-www-form-urlencoded","USER-AGENT":None,"ACCEPT":None ,"Content-Length": str(len(content)) }, verify=False)	
	print response.text
	assert response.status_code == 200
	return response.text


send_post("ciao",url)