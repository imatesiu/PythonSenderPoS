import requests
import time
import xml.etree.ElementTree
from datetime import datetime
from datetime import timedelta
import xml.etree.ElementTree as ET
import sys
import urllib2, base64
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import re
import json
import csv
import fileinput
import hmac
import hashlib
from xml.dom import minidom

set_ip_apparato = "146.48.84.159"

def xmltodate(xml):
	root = ET.fromstring(xml)
	a = (root.findall(".//extraInfo"))
	text = a[0].text
	datet = datetime.strptime(text, '%d%m%Y%H%M%S')
	return datet
	#print res

def dateplus(date):
	end_date = date + timedelta(days=1)
	return end_date.strftime('%d%m%Y')


def createnewdata(xml):
	da = xmltodate(xml)
	r = dateplus(da)
	print r
	data4 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><SetEcrDate><SETDATE><DATE>"+r+"</DATE><TIME>010000</TIME></SETDATE></SetEcrDate></soap:Body></soap:Envelope>"
	return data4

def send_post(content,set_ip_apparato):
	response = requests.post('http://'+set_ip_apparato+':80/oli_webservice.cgi',data=content,headers={"Content-Type": "text/xml"})
	print response.text
	assert response.status_code == 200
	return response.text
	
def create_E_SALE(iva,amont,scontop):
	E_SALE = "<CMD><E_SALE><OPTYPE>1</OPTYPE><BARCODETYPE/><NUMBER>"+iva+"</NUMBER><LISTPRICE>1</LISTPRICE><SALETYPE>1</SALETYPE><DESCRIPTION/><AMOUNT>"+amont+"</AMOUNT><QUANTITY_1/><QUANTITY_2/><QUANTITY_3/><QUANTITY_4/><M_QUANTITY/><S_QUANTITY/><RAEETYPE/><RAEEVALUE/></E_SALE></CMD>"
	E_DISCOUNT = ""
	if(float(scontop.replace(",","."))>0):
		E_DISCOUNT = "<CMD><E_DISCOUNT><P_TYPE>1</P_TYPE><NUMBER>2</NUMBER><DESCRIPTION>Sconto</DESCRIPTION><AMOUNT>"+scontop+"</AMOUNT></E_DISCOUNT></CMD>"
	return E_SALE+E_DISCOUNT
	
def create_E_PAYMENT(amount_contanti, amount_carta, amount_tik, amount_ass, amount_nr):
	E_PAYMENT_C=E_PAYMENT_Carta=E_PAYMENT_Ass=E_PAYMENT_T=E_PAYMENT_NR = ""
	if(float(amount_contanti.replace(",","."))>0):
		E_PAYMENT_C = "<CMD><E_PAYMENT><P_TYPE>1</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>Contanti</DESCRIPTION><AMOUNT>"+amount_contanti+"</AMOUNT><CUSTOMERACCOUNT/></E_PAYMENT></CMD>"
	if(float(amount_carta.replace(",","."))>0):
		E_PAYMENT_Carta = "<CMD><E_PAYMENT><P_TYPE>4</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>Cartadicredito</DESCRIPTION><AMOUNT>"+amount_carta+"</AMOUNT></E_PAYMENT></CMD>"
	if(float(amount_ass.replace(",","."))>0):
		E_PAYMENT_Ass = "<CMD><E_PAYMENT><P_TYPE>2</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>Assegno</DESCRIPTION><AMOUNT>"+amount_ass+"</AMOUNT></E_PAYMENT></CMD>"
	if(float(amount_tik.replace(",","."))>0):
		E_PAYMENT_T = "<CMD><E_PAYMENT><P_TYPE>6</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>Ticket</DESCRIPTION><AMOUNT>"+amount_tik+"</AMOUNT></E_PAYMENT></CMD>"
	if(float(amount_nr.replace(",","."))>0):
		E_PAYMENT_NR = "<CMD><E_PAYMENT><P_TYPE>5</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>NonRiscosso</DESCRIPTION><AMOUNT>"+amount_nr+"</AMOUNT></E_PAYMENT></CMD>"
	return E_PAYMENT_C+E_PAYMENT_Carta+E_PAYMENT_Ass+E_PAYMENT_T+E_PAYMENT_NR
	
def creascontrino(z,data,ora,ved,ndoc,set_ip_apparato):
	documentocommerciale = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><soap:Envelope xmlns:soap=\"http://wwww3org/2001/12/soap-envelope\"><soap:Body><EcrTickets>"+ved+"</EcrTickets></soap:Body></soap:Envelope>"
	print documentocommerciale
	send_post(documentocommerciale,set_ip_apparato)


def tabellaiva(iva):
	ivas = {'22,00':1, '10,00':2, '4,00' : 3 , 'EE':4, 'NS':5,'NI':6,'ES':7,'RM':8,'AL':9}
	return str(ivas.get(iva))
	
def read(filename):
	spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
	header = spamReader[0]
	del spamReader[0]
	return spamReader

def readers(data,ora,z,set_ip_apparato):
	spamReader = read(sys.argv[1])
	nline = 0
	prev = {}
	prev2 = {}
	taxs = []
	amount = 0
	ndoc = 1
	print "#####"
	for line in spamReader:
		importosenzasconto = line[0]
		importoscontato = line[1]
		imponibile = line[2]
		imposta = line[3]
		aliquota = line[4]
		percentualesconto = line[5]
		valoresconto = line[6]
		tipodocumento = line[7]
		importosenzasconto2 = line[9]
		importoscontato2 = line[10]
		imponibile2 = line[11]
		imposta2 = line[12]
		aliquota2 = line[13]
		percentualesconto2 = line[14]
		valoresconto2 = line[15]
		tipodocumento2 = line[16]
		rif = line[8]
		referenceClosurenumber = -1
		referenceDocnumber = -1
		doctype = 1
		if('-' in rif ):
			rifsplit = rif.split("-")
			typ = rifsplit[0]
			rifDoc = rifsplit[1]
			referenceClosurenumber = z
			referenceDocnumber = rifDoc
			if(typ == "5"):
				doctype = 5
			if(typ == "3"):
				doctype = 3	
		current = create_E_SALE(tabellaiva(aliquota),importosenzasconto,percentualesconto)
		current2 = create_E_SALE(tabellaiva(aliquota2),importosenzasconto2,percentualesconto2)
		nline +=1
		if(tipodocumento!="TOTALE"):
			#taxs = createTAX(importoscontato,imposta,aliquota,importoscontato2,imposta2,aliquota2,imponibile,imponibile2) 
			prev = current
			prev2 = current2
		else:	
			pagementoC = line[18]
			pagementoE = line[19]
			pagementoCred = line[20]
			totale = line[21]
			resto = line[22]
			tk = line[23]
			assegno = line[24]
			pagare = create_E_PAYMENT(pagementoC, pagementoE, tk, assegno, pagementoCred)
			if(doctype==1):
				ved =  prev+prev2+pagare
				newtk = creascontrino(z,data,ora,ved,ndoc,set_ip_apparato)
			else:
				ved =  prev+prev2
				#newtk = crea_rettifica(z,data,ora,tok,ved,ndoc,referenceClosurenumber,referenceDocnumber,doctype)
			ndoc+=1
			#data = dateminus(data,ora)
		if(ndoc==15):
			break

	
def send_documentocommerciale(set_ip_apparato):
	documentocommerciale = "<?xmlversion=\"1.0\"encoding=\"UTF-8\"?><soap:Envelopexmlns:soap=\"http://wwww3org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD><E_SALE><OPTYPE>1</OPTYPE><BARCODETYPE/><NUMBER>1</NUMBER><LISTPRICE>1</LISTPRICE><SALETYPE>1</SALETYPE><DESCRIPTION/><AMOUNT>10</AMOUNT><QUANTITY_1/><QUANTITY_2/><QUANTITY_3/><QUANTITY_4/><M_QUANTITY/><S_QUANTITY/><RAEETYPE/><RAEEVALUE/></E_SALE></CMD><CMD><E_DISCOUNT><P_TYPE>2</P_TYPE><NUMBER>2</NUMBER><DESCRIPTION>Sconto</DESCRIPTION><AMOUNT>8,00</AMOUNT></E_DISCOUNT></CMD><CMD><E_PAYMENT><P_TYPE>1</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>PAGAMENTO</DESCRIPTION><AMOUNT>0,50</AMOUNT><CUSTOMERACCOUNT/></E_PAYMENT></CMD><CMD><E_PAYMENT><P_TYPE>4</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>Pagamentocartadicredito</DESCRIPTION><AMOUNT>0,50</AMOUNT></E_PAYMENT></CMD><CMD><E_PAYMENT><P_TYPE>2</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>Assegno</DESCRIPTION><AMOUNT>0,50</AMOUNT></E_PAYMENT></CMD><CMD><E_PAYMENT><P_TYPE>6</P_TYPE><NUMBER>1</NUMBER><DESCRIPTION>Ticket</DESCRIPTION><AMOUNT>0,50</AMOUNT></E_PAYMENT></CMD></EcrTickets></soap:Body></soap:Envelope>"
	send_post(documentocommerciale,set_ip_apparato)
		
		
def send_documentocommerciale2(set_ip_apparato):
	documentocommerciale = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD>...<E_SALE>..<OPTYPE>1</OPTYPE>....<BARCODETYPE></BARCODETYPE>..<NUMBER>1</NUMBER>..<LISTPRICE>1</LISTPRICE>..<SALETYPE>1</SALETYPE>..<DESCRIPTION></DESCRIPTION>..<AMOUNT>1</AMOUNT>..<QUANTITY_1></QUANTITY_1>..<QUANTITY_2></QUANTITY_2>..<QUANTITY_3></QUANTITY_3>..<QUANTITY_4></QUANTITY_4>..<M_QUANTITY></M_QUANTITY>..<S_QUANTITY></S_QUANTITY>..<RAEETYPE></RAEETYPE>..<RAEEVALUE></RAEEVALUE>.</E_SALE></CMD><CMD>...<E_PAYMENT>..<P_TYPE>1</P_TYPE>...<NUMBER>1</NUMBER>...<DESCRIPTION>PAGAMENTO</DESCRIPTION>...<AMOUNT></AMOUNT>....<CUSTOMERACCOUNT></CUSTOMERACCOUNT>...</E_PAYMENT></CMD></EcrTickets></soap:Body></soap:Envelope>"
	send_post(documentocommerciale,set_ip_apparato)

def send_zfiscale( set_ip_apparato):
	zfiscale = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><ExecuteReport>.<PRINTREP>1</PRINTREP>.<REPTYPE>1</REPTYPE>.<REPNUM>10</REPNUM>.</ExecuteReport></soap:Body></soap:Envelope>"
	send_post(zfiscale,set_ip_apparato)

def create_send_new_data(self,  set_ip_apparato):
	getdate = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD><GETDATE></GETDATE></CMD></EcrTickets></soap:Body></soap:Envelope>"
	xml = send_post(getdate,set_ip_apparato)
	d = str(xml)
	dmsg = createnewdata(d)
	send_post(dmsg,set_ip_apparato)
	send_post(dmsg,set_ip_apparato)

	

ved = readers(0,0,0,set_ip_apparato)
exit(0)

documentocommerciale = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD>...<E_SALE>..<OPTYPE>1</OPTYPE>....<BARCODETYPE></BARCODETYPE>..<NUMBER>1</NUMBER>..<LISTPRICE>1</LISTPRICE>..<SALETYPE>1</SALETYPE>..<DESCRIPTION></DESCRIPTION>..<AMOUNT>1</AMOUNT>..<QUANTITY_1></QUANTITY_1>..<QUANTITY_2></QUANTITY_2>..<QUANTITY_3></QUANTITY_3>..<QUANTITY_4></QUANTITY_4>..<M_QUANTITY></M_QUANTITY>..<S_QUANTITY></S_QUANTITY>..<RAEETYPE></RAEETYPE>..<RAEEVALUE></RAEEVALUE>.</E_SALE></CMD><CMD>...<E_PAYMENT>..<P_TYPE>1</P_TYPE>...<NUMBER>1</NUMBER>...<DESCRIPTION>PAGAMENTO</DESCRIPTION>...<AMOUNT></AMOUNT>....<CUSTOMERACCOUNT></CUSTOMERACCOUNT>...</E_PAYMENT></CMD></EcrTickets></soap:Body></soap:Envelope>"

zfiscale = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><ExecuteReport>.<PRINTREP>1</PRINTREP>.<REPTYPE>1</REPTYPE>.<REPNUM>10</REPNUM>.</ExecuteReport></soap:Body></soap:Envelope>"

changedate = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD><GETDATE></GETDATE></CMD></EcrTickets></soap:Body></soap:Envelope>"

day = 6
data2 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><SetEcrDate><SETDATE><DATE>08102017</DATE><TIME>010000</TIME></SETDATE></SetEcrDate></soap:Body></soap:Envelope>"

def create_data(day):
	da = str(day).zfill(2)
	data4 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><SetEcrDate><SETDATE><DATE>"+da+"112017</DATE><TIME>010000</TIME></SETDATE></SetEcrDate></soap:Body></soap:Envelope>"
	return data4


num = 2
while True:
	if num == 1 or num == 40:
			xml = send_post(changedate)
			d = str(xml)
			dmsg = createnewdata(d)
			send_post(dmsg)
			send_post(dmsg)
			num = 2
	send_post(documentocommerciale)
	send_post(zfiscale)
	print num
	time.sleep(200)
	num +=1
