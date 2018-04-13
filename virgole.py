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
import time
from xml.dom import minidom

def read(filename):
	spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
	header = spamReader[0]
	del spamReader[0]
	return spamReader


spamReader = read(sys.argv[1])
#head = spamReader[0]
#del spamReader[0]

nline = 0
prev = {}
prev2 = {}
taxs = []
amount = 0
print "#####"
for line in spamReader:
	riga = ""
	for ele in line:
		if not bool(re.search(',', ele)) and (bool(re.search('\d+', ele)) ) and not bool(re.search('\D', ele))and len(ele)>0:
			riga += ele+",00;"
		else:
			riga += ele+";"
			
	print riga