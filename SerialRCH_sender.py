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



def read(filename):
	spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
	header = spamReader[0]
	header2 = spamReader[1]
	del spamReader[0]
	del spamReader[0]
	return spamReader
	
def readers():
	spamReader = read(sys.argv[1])
	nline = 0
	prev = {}
	prev2 = {}
	taxs = []
	amount = 0
	ndoc = 1
	print "#####"
	for line in spamReader:
		print line
		tipo = line[7]
		if tipo == "DC":
			importosenzasconto = line[0]
			importoscontato = line[1]
			imponibile = line[2]
			imposta = line[3]
			aliquota = line[4]
			percentualesconto = line[5]
			valoresconto = line[6]
			tipodocumento = line[7]
			exit(0)
readers()


	
