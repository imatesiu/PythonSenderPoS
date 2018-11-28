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


def datem(date):
	text = str(date)
	datet = datetime.datetime.strptime(str.strip(text), '%d/%m/%Y')
	return datet.strftime('%d%m%Y')

def read(filename):
	spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
	header = spamReader[0]
	header2 = spamReader[1]
	del spamReader[0]
	del spamReader[0]
	return spamReader

def aliquotareparto(aliquota):
	if("4" in aliquota):
		return 1
	if("10" in aliquota):
		return 2
	if("22" in aliquota):
		return 3
	if("EE" in aliquota):
		return 4
	if("NS" in aliquota):
		return 5
	if("NI" in aliquota):
		return 6
	if("ES" in aliquota):
		return 7
	if("RM" in aliquota):
		return 8
	if("AL" in aliquota):
		return 9
	

def df(line,pimp):
	res = ""
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
		res +=("=R%s/$%s\n\r" % (aliquotareparto(aliquota) ,str(importosc).replace(".","")))
		if len(percentualesconto)>1:
			psconto = float(percentualesconto.replace(",","."))
			if psconto>0:
				res += "=%/*"+str(psconto)+"\n\r"
		else:
			if len(valoresconto)>1 and len(vsconto)>1:
				res += "=S\n\r"
				vsconto = float(valoresconto.replace(",","."))
				res += "=V/$"+str(vsconto).replace(".","")+"\n\r"
	else:
		if(pimp>0):
			res += "=a"
		else:
			res += "=K"
	return res

def df2(line,pimp):
	res = ""
	importosenzasconto = line[0]
	importoscontato = line[1]
	imponibile = line[2]
	imposta = line[3]
	aliquota = line[4]
	percentualesconto = line[5]
	vsconto = line[6]
	valoresconto = line[8]
	tipodocumento = line[7]
	importosc = float(importoscontato.replace(",","."))
	if(importosc>0):
		res +=("3/N/PRODOTTO~SERVIZIO//1.00/%s/%s//" % (str("%.2f" %(importosc)), aliquotareparto(aliquota)))
	return res
	
def readers():
	spamReader = read(sys.argv[1])
	nline = 0
	prev = ""
	prev2 = {}
	taxs = []
	rifn = ""
	ndoc = 0
	pimp = 0
	ddc = ""
	print "#####"
	for line in spamReader:
		#print line
		tipo = line[7]
		if tipo == "ADC":
			if ddc == "ADC":
				data = line[8]
				#df(line,pimp)
				split = rifn.split("_")
				print("+/1/%s/%s/%s/" % (datem(data) ,  split[0], split[1] ))
				print 
			else:
				rifn = line[8]
				#df(line,pimp)
		if tipo == "RDC":
			if ddc == "RDC":
				data = line[8]
				split = rifn.split("_")
				print("-/%s/%s/%s/" % (datem(data) ,  split[0], split[1] ))
				print prev
				print df2(line,pimp)
				print "5/1/0////"
				print 
			else:
				rifn = line[8]
				prev = df2(line,pimp)
		if tipo == "DC":
			importosenzasconto = line[0]
			importoscontato = line[1]
			imponibile = line[2]
			imposta = line[3]
			aliquota = line[4]
			percentualesconto = line[5]
			valoresconto = line[8]
			tipodocumento = line[7]
			importosc = float(importosenzasconto.replace(",","."))
			#3/S/PRODOTTO~SERVIZIO//1.00/1.00/1//
			if(importosc>0):
				print("3/S/PRODOTTO~SERVIZIO//1.00/%s/%s//" % (str("%.2f" %(importosc)), aliquotareparto(aliquota)))
				if len(percentualesconto.strip())>1:
					psconto = float(percentualesconto.replace(",","."))
					#4/10.00///0/0/0/ 
					if psconto>0:
						print "4/%s///0/0/0/" % str("%.2f" %(psconto))
				else:
					if len(valoresconto)>1:
						vsconto = float(valoresconto.replace(",","."))
						if vsconto>0:
							print "4/%s///0/1/1/" % str("%.2f" %(vsconto))
			else:
				if(pimp>0):
					print "=a"
				else:
					print "+"
			
			pimp = importosc
		if tipo == "P":
			ticket = line[0]
			bancomat = line[1]
			Credito = line[2]
			Assegni = line[3]
			CartaC = line[4]
			Contanti = line[5]
			#
			if len(ticket)>0:
				itk = float(ticket.replace(",","."))
				if itk>0:
					print ("5/3/%s////" % (str("%.2f" %(itk)))) 
			if len(bancomat)>0:
				itk = float(bancomat.replace(",","."))
				if itk>0:
					print ("5/4/%s////" % (str("%.2f" %(itk)))) 
			if len(Credito)>0:
				itk = float(Credito.replace(",","."))
				if itk>0:
					print ("5/2/%s////" % (str("%.2f" %(itk)))) 
			if len(Assegni)>0:
				itk = float(Assegni.replace(",","."))
				if itk>0:
					print ("5/6/%s////" % (str("%.2f" %(itk)))) 
			if len(CartaC)>0:
				itk = float(CartaC.replace(",","."))
				if itk>0:
					print ("5/5/%s////" % (str("%.2f" %(itk)))) 
			if len(Contanti)>0:
				itk = float(Contanti.replace(",","."))
				if itk>0:
					print ("5/1/%s////" % (str("%.2f" %(itk)))) 
			ndoc+=1
			print
		ddc = tipo
		if ndoc == 15:
			exit(0)
			#exit(0)Ticket;Bancomat;Credito;Assegni;CartaC;Contanti
readers()


	
