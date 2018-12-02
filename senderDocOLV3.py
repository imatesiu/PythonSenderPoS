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

'''import serial

def serial(p):
	serial = serial.Serial(port = p, baudrate = 9600, parity = serial.None, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS,  xonxoff=True, timeout=2)
'''

def read(filename):
	spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
	header = spamReader[0]
	header2 = spamReader[1]
	del spamReader[0]
	del spamReader[0]
	return spamReader
'''


1 Pagamento con Contanti
2 Pagamento con Assegni
3 Pagamento con carta di credito
4 Pagamento con Buoni 
5 Pagamento a credito (equivalente al comando 12M)
6* Pagamento con Ticket (Subtender1)
7* Pagamento con Subtender2
8* Pagamento con Subtender3
9* Pagamento con Subtender4'''

def aliquotareparto(aliquota):
	if("4" in aliquota):
		return 1
	if("10" in aliquota):
		return 2
	if("22" in aliquota):
		return 3
	if("EE" in aliquota):
		return 4
	if("ES" in aliquota):
		return 5
	if("AL" in aliquota):
		return 6
	if("RM" in aliquota):
		return 7
	if("NS" in aliquota):
		return 8
	if("NI" in aliquota):
		return 8

def df(line,pimp):
	importosenzasconto = line[0]
	importoscontato = line[1]
	imponibile = line[2]
	imposta = line[3]
	aliquota = line[4]
	percentualesconto = line[5]
	vsconto = line[6]
	valoresconto = line[8]
	tipodocumento = line[7]
	importosc = float(importosenzasconto.replace(",","."))
	if(importosc>0):
		print("%sH%sR" % (str(importosc).replace(".",""),aliquotareparto(aliquota) ))
		if len(percentualesconto)>1:
			psconto = float(percentualesconto.replace(",","."))
			print str(psconto)+"*1M"
		else:
			if len(valoresconto)>1 and len(vsconto)>1:
				#print "=S"
				vsconto = float(valoresconto.replace(",","."))
				print str(vsconto).replace(".","")+"3M"
	else:
		if(pimp>0):
			print "=a"
		else:
			print "=K"
	
def readers():
	spamReader = read(sys.argv[1])
	nline = 0
	prev = {}
	prev2 = {}
	taxs = []
	rifn = ""
	ndoc = 0
	pimp = 0
	ddc = ""
	print "1322;2"
	for line in spamReader:
		#print line
		tipo = line[7]
		if tipo == "ADC":
			if ddc == "ADC":
				data = line[8]
				#df(line,pimp)
				#print rifn+";"+data
			else:
				rifn = line[8]
				#df(line,pimp)
		if tipo == "RDC":
			if ddc == "RDC":
				data = line[8]
				#print rifn+";"+data
			else:
				rifn = line[8]
		if tipo == "DC":
			importosenzasconto = line[0]
			importoscontato = line[1]
			imponibile = line[2]
			imposta = line[3]
			aliquota = line[4]
			percentualesconto = line[5]
			vsconto = line[6]
			valoresconto = line[8]
			tipodocumento = line[7]
			importosc = float(importosenzasconto.replace(",","."))
			if(importosc>0):
				#1325;10,00;1 PLU_1;0
				print("1325;%s;DESC;%s" % ( "{0:.2f}".format(importosc).replace(".",","),aliquotareparto(aliquota) ))
				if len(percentualesconto)>1:
					psconto = float(vsconto.replace(",","."))
					if(psconto>0):
						print ("1327;-%s;;" % ( "{0:.2f}".format(psconto).replace(".","")))
				else:
					if len(valoresconto)>1 and len(vsconto)>1:
						#print "=S"
						vsconto = float(valoresconto.replace(",","."))
						if(vsconto>0):
							print "1332;2"
							print ("1327;-%s;;" % ( "{0:.2f}".format(vsconto).replace(".","")))
			else:
				if(pimp>0):
					print "1331"
				else:
					print "1324"
			
			pimp = importosc
		if tipo == "P":
			ticket = line[0]
			bancomat = line[1]
			Credito = line[2]
			Assegni = line[3]
			CartaC = line[4]
			Contanti = line[5]
			if len(ticket)>0:
				itk = float(ticket.replace(",","."))
				if itk>0:
					print "{0:.2f}".format(itk)+"H6T"
			if len(bancomat)>0:
				itk = float(bancomat.replace(",","."))
				if itk>0:
					print "{0:.0f}".format(itk*100)+"H3T"
			if len(Credito)>0:
				itk = float(Credito.replace(",","."))
				if itk>0:
					print "{0:.0f}".format(itk*100)+"H5T"
			if len(Assegni)>0:
				itk = float(Assegni.replace(",","."))
				if itk>0:
					print "{0:.0f}".format(itk*100)+"H2T"
			if len(CartaC)>0:
				itk = float(CartaC.replace(",","."))
				if itk>0:
					print "{0:.0f}".format(itk*100)+"H3T"
			if len(Contanti)>0:
				itk = float(Contanti.replace(",","."))
				if itk>0:
					print ("1329;%s;%s" %( "{0:.2f}".format(itk).replace(".",","), "CONTANTI"))
			ndoc+=1
			print "1323"
			print 			
			print "1322;2"
		ddc = tipo
		if ndoc == 15:
			exit(0)
			#exit(0)Ticket;Bancomat;Credito;Assegni;CartaC;Contanti
readers()


	
