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


user = "AB120002"
if(len(sys.argv)>2):
	 user = sys.argv[2] 
password = "passwordcassa"
set_ip_server = "192.168.1.110"
matricola = "88S25000027"



import urllib2, base64



def createhash2(content):
	sha256 = hashlib.sha256()
	sha256.update(content)
	return base64.b64encode(sha256.digest())


def send_post(content, url):
	print "https://"+set_ip_server+"/"+url
	base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
	pem = 'CASogeiTest.cer'
	response = requests.post('https://'+set_ip_server+'/'+url,data=content,headers={"Content-Type": "application/xml", "Authorization": "BASIC %s" % base64string  }, verify=False)	
	print response.text
	assert response.status_code == 200
	return response.text
	
def send_get(content, url):
	print "https://"+set_ip_server+"/"+url
	base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
	pem = 'CASogeiTest.cer'
	response = requests.get('https://'+set_ip_server+'/'+url,data=content,headers={"Content-Type": "application/xml", "Authorization": "BASIC %s" % base64string  }, verify=False)	
	print response.text
	assert response.status_code == 200
	return response.text

def createhash(content):
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()

def hmacsha256(key,mess):
	digest = hmac.new(bytes(key).encode('utf-8'), bytes(mess).encode('utf-8'), digestmod=hashlib.sha256).digest()
	signature = base64.b64encode(digest)
	return signature 

def send_stato_server():
	url = "ServerRT/ver1/api/richiesta/stato/server"
	content = ""#"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura></Chiusura>"
	send_post(content,url)

def send_stato_db():
	url = "ServerRT/ver1/api/richiesta/stato/db"
	content = ""#"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura></Chiusura>"
	send_post(content,url)

    
def send_chiusura_cassa():
	url = "ver1/api/richiesta/chiusura"
	content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura></Chiusura>"
	send_post(content,url)

def send_chiusura_server():
	url = "ServerRT/ver1/api/richiesta/chiusura"
	content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura><ServerRT/></Chiusura>"
	send_post(content,url)
	
def send_forza_chiusura_server():
	url = "ServerRT/ver1/api/richiesta/chiusura"
	content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura><ForzaChiusura/></Chiusura>"
	send_post(content,url)	
    
def send_apertura_cassa():
	url = "ServerRT/ver1/api/richiesta/apertura"
	content = "<AperturaPuntoCassa/>"
	res = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><ConfermaAperturaPuntoCassa><UltimaChiusura>0000</UltimaChiusura></ConfermaAperturaPuntoCassa>"
	response = send_post(content,url)
	mydoc = minidom.parseString(response)
	UltimaChiusura = mydoc.getElementsByTagName("UltimaChiusura")
	return UltimaChiusura[0].firstChild.data

def send_ric_token_cassa():
	url = "ver1/api/richiesta/token"
	content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><RichiestaToken></RichiestaToken>"
	res = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><RestituzioneToken><Token>98C6F5255688BB32393033323031383030303130303030303030303030303030</Token><MatricolaRT>88S25000010</MatricolaRT><PuntoCassa>AB120001</PuntoCassa><DataOra><Data>29032018</Data><Ora>17:47:26</Ora></DataOra></RestituzioneToken>"
	response = send_post(content,url)
	mydoc = minidom.parseString(response)
	Tokens = mydoc.getElementsByTagName("Token")
	Datas = mydoc.getElementsByTagName("Data")
	Oras = mydoc.getElementsByTagName("Ora")
	print Datas[0].firstChild.data
	print Oras[0].firstChild.data
	return Tokens[0].firstChild.data,Datas[0].firstChild.data,Oras[0].firstChild.data
	
def send_documento(scontrino,cdcp,tk):
	url = "ver1/api/invio/documento"
	content = "<?xmlversion=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Documento><CCDCPrecedente>"+cdcp+"</CCDCPrecedente><PuntoCassa>"+user+"</PuntoCassa>"+scontrino+"<CCDC>"+tk+"</CCDC></Documento>"
	#print content
	cc = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Documento><CCDCPrecedente>"+cdcp+"</CCDCPrecedente><PuntoCassa>"+user+"</PuntoCassa>"+scontrino+"<CCDC>"+tk+"</CCDC></Documento>"
	#res = "<?xmlversion=\"1.0\" encoding=\"UTF-8\"?><ConfermaDocumento><Data>29032018</Data><TotaleGiornaliero>12,20</TotaleGiornaliero><IdentificativoDocumento><NumeroAzzeramento>0001</NumeroAzzeramento><NumeroDocumento>0001</NumeroDocumento></IdentificativoDocumento></ConfermaDocumento>"
	print cc
	response = send_post(cc,url)
	mydoc = minidom.parseString(response)
	NumeroAzzeramentos = mydoc.getElementsByTagName("NumeroAzzeramento")
	NumeroDocumentos = mydoc.getElementsByTagName("NumeroDocumento")
	TotaleGiornalieros = mydoc.getElementsByTagName("TotaleGiornaliero")
	print NumeroAzzeramentos[0].firstChild.data
	print NumeroDocumentos[0].firstChild.data
	print TotaleGiornalieros[0].firstChild.data


def crea_rettifica(chiusura,data,ora,tkold,ved,ndoc,referenceClosurenumber,referenceDocnumber,doctype):
	annullo = 1 #annullo
	if(doctype == 3):
		annullo = 0 #reso
	rettifica = "<RettificaScontrino><Data>"+data+"</Data><Ora>"+ora+"</Ora><NumeroDocumento>"+str(ndoc).zfill(4)+"</NumeroDocumento><NumeroAzzeramento>"+str(chiusura).zfill(4)+"</NumeroAzzeramento><RiferimentoDocumento><DataRegistrazione>"+data+"</DataRegistrazione><OrarioRegistrazione>"+ora+"</OrarioRegistrazione><NumeroProgressivo>"+str(referenceClosurenumber).zfill(4)+"-"+str(referenceDocnumber).zfill(4)+"</NumeroProgressivo></RiferimentoDocumento>"+ved+"<Annullamento>"+str(annullo)+"</Annullamento></RettificaScontrino>"
	cont = tkold+matricola+user+rettifica
	tk = createhash(cont)
	send_documento(rettifica,tkold,tk.upper())
	return tk.upper()



def read(filename):
	spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
	header = spamReader[0]
	del spamReader[0]
	return spamReader

def readers(tok,data,ora):
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
		vendita1 = "<Dettagli><Vendita><Descrizione>Articolo1</Descrizione><Importo>"+importosenzasconto+"</Importo><Quantita>1</Quantita><PrezzoUnitario>"+importosenzasconto+"</PrezzoUnitario><CodiceIVA><Aliquota>"+aliquota+"</Aliquota></CodiceIVA></Vendita></Dettagli>"
		vendita2 = "<Dettagli><Vendita><Descrizione>Articolo2</Descrizione><Importo>"+importosenzasconto2+"</Importo><Quantita>1</Quantita><PrezzoUnitario>"+importosenzasconto2+"</PrezzoUnitario><CodiceIVA><Aliquota>"+aliquota2+"</Aliquota></CodiceIVA></Vendita></Dettagli>"
		if("N" in aliquota  ):
			vendita1 = vendita1.replace("Aliquota","CodiceEsenzioneIVA",2)
		if("N" in aliquota2  ):
			vendita2 = vendita2.replace("Aliquota","CodiceEsenzioneIVA",2)
		sconto1 = ""
		sconto2 = ""
		if float(valoresconto.replace(",","."))>0:
			sconto1 = "<Dettagli><ModificatoreSuArticolo><Descrizione>Sconto</Descrizione><Importo>"+valoresconto+"</Importo><Segno>-</Segno><CodiceIVA><Aliquota>"+aliquota+"</Aliquota></CodiceIVA></ModificatoreSuArticolo></Dettagli>"
			if("N" in aliquota  ):
				sconto1 = sconto1.replace("Aliquota","CodiceEsenzioneIVA",2)
		if float(valoresconto2.replace(",","."))>0:
			sconto2 = "<Dettagli><ModificatoreSuArticolo><Descrizione>Sconto</Descrizione><Importo>"+valoresconto2+"</Importo><Segno>-</Segno><CodiceIVA><Aliquota>"+aliquota2+"</Aliquota></CodiceIVA></ModificatoreSuArticolo></Dettagli>"
			if("N" in aliquota  ):
				sconto2 = sconto2.replace("Aliquota","CodiceEsenzioneIVA",2)
		current = vendita1+sconto1
		current2 = vendita2+sconto2
		nline +=1
		if(tipodocumento!="TOTALE"):
			taxs = createTAX(importoscontato,imposta,aliquota,importoscontato2,imposta2,aliquota2) 
			prev = current
			prev2 = current2
		else:	
			pagementoC = line[18]
			pagementoE = line[19]
			pagementoCred = line[20]
			pagare = "<Dettagli><Pagamento><Descrizione>Contanti</Descrizione><Importo>"+pagementoC+"</Importo><Tipo>PC</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Elettronico</Descrizione><Importo>"+pagementoE+"</Importo><Tipo>PE</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Ticket</Descrizione><Importo>"+pagementoCred+"</Importo><Tipo>TK</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>NonRiscosso</Descrizione><Importo>0,00</Importo><Tipo>NR</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Resto</Descrizione><Importo>0,00</Importo><Tipo>RS</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Assegno</Descrizione><Importo>0,00</Importo><Tipo>AS</Tipo></Pagamento></Dettagli>"
			totale = "<Totale>"+line[1]+"</Totale>"
			#print doctype
			if(doctype==1):
				ved =  prev+prev2+pagare+totale+taxs
				newtk = creascontrino2(z,data,ora,tok,ved,ndoc)
			else:
				ved =  prev+prev2+totale+taxs
				newtk = crea_rettifica(z,data,ora,tok,ved,ndoc,referenceClosurenumber,referenceDocnumber,doctype)
			tok = newtk
			ndoc+=1
		if(ndoc==3):
			break


def createTAX(importoscontato,imposta,aliquota,importoscontato2,imposta2,aliquota2):
	tax = ""
	if aliquota2!=aliquota:
		tax1 = "<CorrispettiviIVA><Importo>"+importoscontato+"</Importo><BaseImponibile>"+str(float(importoscontato.replace(",","."))-float(imposta.replace(",","."))).replace(".",",")+"</BaseImponibile><Imposta>"+imposta+"</Imposta><CodiceIVA><Aliquota>"+aliquota+"</Aliquota></CodiceIVA></CorrispettiviIVA>"
		tax2 = "<CorrispettiviIVA><Importo>"+importoscontato2+"</Importo><BaseImponibile>"+str(float(importoscontato2.replace(",","."))-float(imposta2.replace(",","."))).replace(".",",")+"</BaseImponibile><Imposta>"+imposta2+"</Imposta><CodiceIVA><Aliquota>"+aliquota2+"</Aliquota></CodiceIVA></CorrispettiviIVA>"
		if("N" in aliquota  ):
			tax1 = tax1.replace("Aliquota","CodiceEsenzioneIVA",2)			
		if("N" in aliquota2 ):
			tax2 = tax2.replace("Aliquota","CodiceEsenzioneIVA",2)
		tax = tax1+tax2
	else:
		imp = float(importoscontato)
		impost = float(imposta)
		imp2 = float(importoscontato2)
		impost2 = float(imposta2)
		tax = "<CorrispettiviIVA><Importo>"+(imp+imp2)+"</Importo><BaseImponibile>"+(imp+imp2)-(impost+impost2)+"</BaseImponibile><Imposta>"+(impost+impost2)+"</Imposta><CodiceIVA><Aliquota>"+aliquota+"</Aliquota></CodiceIVA></CorrispettiviIVA>"
		if("N" in aliquota ):
			tax = tax.replace("Aliquota","CodiceEsenzioneIVA",2)	
	return tax


def creascontrino(chiusura,data,ora,tkold):
	scontrino = "<Scontrino><Data>"+data+"</Data><Ora>"+ora+"</Ora><NumeroDocumento>0001</NumeroDocumento><NumeroAzzeramento>"+str(chiusura).zfill(4)+"</NumeroAzzeramento><Dettagli><Vendita><Descrizione>Articolo16</Descrizione><Importo>10,00</Importo><Quantita>1</Quantita><PrezzoUnitario>10,00</PrezzoUnitario><CodiceIVA><Aliquota>10,00</Aliquota></CodiceIVA></Vendita></Dettagli><Dettagli><Pagamento><Descrizione>Contanti</Descrizione><Importo>10,00</Importo><Tipo>PC</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Elettronico</Descrizione><Importo>0,00</Importo><Tipo>PE</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Ticket</Descrizione><Importo>0,00</Importo><Tipo>TK</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>NonRiscosso</Descrizione><Importo>0,00</Importo><Tipo>NR</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Resto</Descrizione><Importo>0,00</Importo><Tipo>RS</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Assegno</Descrizione><Importo>0,00</Importo><Tipo>AS</Tipo></Pagamento></Dettagli><Totale>10,00</Totale><CorrispettiviIVA><Importo>10,00</Importo><BaseImponibile>9,09</BaseImponibile><Imposta>0,91</Imposta><CodiceIVA><Aliquota>10,00</Aliquota></CodiceIVA></CorrispettiviIVA></Scontrino>"
	cont = tkold+matricola+user+scontrino
	tk = createhash(cont)
	send_documento(scontrino,tkold,tk.upper())

def creascontrino2(chiusura,data,ora,tkold,ved,ndoc):
	scontrino = "<Scontrino><Data>"+data+"</Data><Ora>"+ora+"</Ora><NumeroDocumento>"+str(ndoc).zfill(4)+"</NumeroDocumento><NumeroAzzeramento>"+str(chiusura).zfill(4)+"</NumeroAzzeramento>"+ved+"</Scontrino>"
	cont = tkold+matricola+user+scontrino
	tk = createhash(cont)
	send_documento(scontrino,tkold,tk.upper())
	return tk.upper()

def loop_HW():
	while True:
		kiusura = send_apertura_cassa()
		z = str(int(kiusura)+1)
		#print str(kiu)
		#exit(0)
		tokenp = send_ric_token_cassa()
		creascontrino(z,tokenp[1],tokenp[2],tokenp[0])
		send_chiusura_cassa()	
		send_chiusura_server()	
		time.sleep(19)
	
def test():
	tok = "A45A220E3535EC9729B6589CDAE361F81B02B45C3C1F546F83014BDEC6952514"
	data = "17042018"
	ora = "23:43"
	creascontrino(23,data,ora,tok)
	
loop_HW()
exit(0)	
send_chiusura_cassa()
#send_forza_chiusura_server()
#exit(0)

#kiusura = send_apertura_cassa()
#doc = "<?xmlversion=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Documento><CCDCPrecedente>98C6F5255688BB30393034323031383132393930303032303030303037343830</CCDCPrecedente><PuntoCassa>AB120002</PuntoCassa><Scontrino><Data>09042018</Data><Ora>14:27</Ora><NumeroDocumento>0001</NumeroDocumento><NumeroAzzeramento>0000</NumeroAzzeramento><Dettagli><Vendita><Descrizione>Articolo 17</Descrizione><Importo>10,00</Importo><Quantita>5</Quantita><PrezzoUnitario>2,00</PrezzoUnitario><CodiceIVA><Aliquota>22,00</Aliquota></CodiceIVA></Vendita></Dettagli><Dettagli><Vendita><Descrizione>Articolo 1</Descrizione><Importo>12,20</Importo><Quantita>2</Quantita><PrezzoUnitario>6,10</PrezzoUnitario><CodiceIVA><CodiceEsenzioneIVA>EE</CodiceEsenzioneIVA></CodiceIVA></Vendita></Dettagli><Dettagli><Pagamento><Descrizione>Contanti</Descrizione><Importo>22,20</Importo><Tipo>PC</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Elettronico</Descrizione><Importo>0,00</Importo><Tipo>PE</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Ticket</Descrizione><Importo>0,00</Importo><Tipo>TK</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Non Riscosso</Descrizione><Importo>0,00</Importo><Tipo>NR</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Resto</Descrizione><Importo>0,00</Importo><Tipo>RS</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Assegno</Descrizione><Importo>0,00</Importo><Tipo>AS</Tipo></Pagamento></Dettagli><Totale>22,20</Totale><CorrispettiviIVA><Importo>10,00</Importo><BaseImponibile>8,20</BaseImponibile><Imposta>1,80</Imposta><CodiceIVA><Aliquota>22,00</Aliquota></CodiceIVA></CorrispettiviIVA><CorrispettiviIVA><Importo>12,20</Importo><BaseImponibile>12,20</BaseImponibile><CodiceIVA><CodiceEsenzioneIVA>EE</CodiceEsenzioneIVA></CodiceIVA></CorrispettiviIVA></Scontrino><CCDC>E969321BEDA3638619CE4F085BCBF00345D6DE6560E60D27D4B3058CD5A995F6</CCDC></Documento>"
#send_post(doc,url = "ver1/api/invio/documento")
#exit(0)
kiusura = send_apertura_cassa()
z = str(int(kiusura)+1)
#print str(kiu)
#exit(0)
tokenp = send_ric_token_cassa()
ved = readers(tokenp[0],tokenp[1],tokenp[2])



send_chiusura_cassa()
send_chiusura_server()
exit(0)


