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
	ndoc = 0
	print "#####"
	for line in spamReader:
		#print line
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
			print "=R1/$"+str(float(importosenzasconto.replace(",","."))).replace(".","")
			if len(percentualesconto)>1:
				psconto = float(percentualesconto.replace(",","."))
				print "=%/*"+str(psconto)
			else:
				if len(valoresconto)>1:
					vsconto = float(valoresconto.replace(",","."))
					print "=V/$"+str(vsconto).replace(".","")
		if tipo == "P":
			ticket = line[0]
			bancomat = line[1]
			Credito = line[2]
			Assegni = line[3]
			CartaC = line[4]
			Contanti = line[5]
			if len(ticket)>0:
				itk = float(ticket.replace(",","."))
				print "=T1${0:.0f}".format(itk*100)
			if len(bancomat)>0:
				itk = float(bancomat.replace(",","."))
				print "=T2${0:.0f}".format(itk*100)
			if len(Credito)>0:
				itk = float(Credito.replace(",","."))
				print "=T3${0:.0f}".format(itk*100)
			if len(Assegni)>0:
				itk = float(Assegni.replace(",","."))
				print "=T4${0:.0f}".format(itk*100)
			if len(CartaC)>0:
				itk = float(CartaC.replace(",","."))
				print "=T5${0:.0f}".format(itk*100)
			if len(Contanti)>0:
				itk = float(Contanti.replace(",","."))
				print "=T${0:.0f}".format(itk*100)
			print "=C"
			ndoc+=1
		if ndoc == 15:
			exit(0)
			#exit(0)Ticket;Bancomat;Credito;Assegni;CartaC;Contanti
readers()


	
