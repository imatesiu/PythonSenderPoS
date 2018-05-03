#!/usr/bin/python
import sys
import urllib2, base64
import ssl
import requests
import time
from base64 import b64encode
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
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
import threading
from Tkinter import *
from ttk import Combobox

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class MiaApp:


		
		
	def __init__(self, genitore):

		
		
		self.mioGenitore = genitore
		self.mioContenitore1 = Frame(genitore)
		self.mioContenitore1.pack()
		
		Label(self.mioContenitore1, text="Matricola: ").grid(row=0,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="Sent to IP: ").grid(row=1,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="Intervallo: ").grid(row=2,pady=5,sticky=W)
		v = StringVar()
		v.set("88S25000026")
		self.e1 = Entry(self.mioContenitore1,textvariable=v)
		v1 = StringVar()
		v1.set("146.48.89.2")#192.168.1.146
		self.e2 = Entry(self.mioContenitore1,textvariable=v1)
		v2 = StringVar()
		v2.set("8")
		self.e3 = Entry(self.mioContenitore1,textvariable=v2)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		
		Label(self.mioContenitore1, text="GT: ").grid(row=3,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="Z: ").grid(row=4,column=0,pady=5,sticky=W)
		v3 = StringVar()
		v3.set("00.00")
		self.e4 = Entry(self.mioContenitore1,textvariable=v3)
		
		v4 = StringVar()
		v4.set("0")
		self.e5 = Entry(self.mioContenitore1,textvariable=v4)
		
		self.e4.grid(row=3, column=1)
		self.e5.grid(row=4, column=1)
		
		self.prove = ("Termiche","Impermeabilita","Vibrazione","DisturbiElettromagnetici","DisturbiCondotti","BatteriaSottoProtezioneSF","AlimentazioneBatteriaSenzaVincoloFiscale","ScaricheElettrostatiche","Guastoemalfunzionamento")
		self.cbp3 = Label(self.mioContenitore1, text='Prova: ')
		self.cbp3.grid(row=5, column=0,pady=5)
		self.cb3 = Combobox(self.mioContenitore1, values=self.prove, state='readonly')
		self.cb3.current(1)  # set selection
		self.cb3.grid(row=5, column=1)

		
		self.pulsante1 = Button(self.mioContenitore1,
														command = self.pulsante1Premuto)
		self.pulsante1.bind("<Button-1>", self.pulsante1Premuto_a)	### (1)
		self.pulsante1.configure(text = "Start", background = "green")
		self.pulsante1.grid(row=6, column=0,pady=25)
		self.pulsante1.focus_force()
		
		
		self.pulsante2 = Button(self.mioContenitore1,
														command = self.pulsante2Premuto)
		self.pulsante2.bind("<Return>", self.pulsante2Premuto)	### (1)
		self.pulsante2.configure(text = "Pause", background = "yellow")
		self.pulsante2.grid(row=6, column=1)
		self.pulsante2.focus_force()
		
		self.pulsante3 = Button(self.mioContenitore1,
														command = self.pulsante3Premuto)
		self.pulsante3.bind("<Return>", self.pulsante3Premuto)	### (1)
		self.pulsante3.configure(text = "Stop", background = "red")
		self.pulsante3.grid(row=6, column=2)
		self.pulsante3.focus_force()
		
		

		self.pulsantee = Button(self.mioContenitore1,
														command = self.pulsanteEPremuto)
		self.pulsantee.bind("<Return>", self.pulsanteEPremuto_a)	### (1)
		self.pulsantee.configure(text = "Chiudi", background = "red")
		self.pulsantee.grid(row=8, column=0)
		
		self.pulsanteinfo = Button(self.mioContenitore1,
														command = self.pulsanteInfoPremuto)
		self.pulsanteinfo.bind("<Return>", self.pulsanteInfoPremuto)	### (1)
		self.pulsanteinfo.configure(text = "Info", background = "green")
		self.pulsanteinfo.grid(row=8, column=2)
		self.pulsanteinfo.focus_force()
		



	def pulsante1Premuto(self):	### (2)
		print "Gestore di eventi 'pulsante1Premuto'"
		#if self.pulsante1["background"] == "green":
		#	self.pulsante1["background"] = "yellow"
		#else:
		#	self.pulsante1["background"] = "green"

	def pulsante2Premuto(self):	### (2)
		print "Gestore di eventi 'pulsante2Premuto'"
		if self.pulsante1["background"] == "green":
			self.pulsante1["background"] = "yellow"
			self.thread.start()
		else:
			self.pulsante1["background"] = "green"
			self.thread.pause()

	def pulsante3Premuto(self):	### (2)
		print "Gestore di eventi 'pulsante2Premuto'"
		self.send_stop(str(self.e1.get()))
		#self.mioGenitore.destroy()
				
		




	def pulsanteEPremuto_a(self, evento):	### (3)
		print "Gestore di eventi 'pulsante2Premuto_a' (un involucro)"

		
	def pulsanteInfoPremuto(self):	### (3)
		self.send_getinfo(str(self.e1.get()))
		
		
	def pulsanteEPremuto(self):	### (3)
		print "Gestore di eventi 'pulsante2Premuto_a' (un involucro)"
		self.mioGenitore.destroy()
		
		
	def send_get(self,ip_server, url, param):
		print "https://"+ip_server+"/"+url+param
		#base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
		#pem = 'CASogeiTest.cer'
		response = requests.get('https://'+ip_server+'/'+url+param,headers={"Content-Type": "application/xml"}, verify=False)
		print response.text
		assert response.status_code == 200
		return response.text
		
	def send_init(self,matricola,gt,z,prova):
		#https://localhost/v1/dispositivi/corrispettivi/init/80M08002493?grantot=28.8&desc=Termiche&z=33
		url = "v1/dispositivi/corrispettivi/init/"
		print type((matricola))
		param = matricola+"?grantot="+gt+"&desc="+prova+"&z="+z
		self.send_get("localhost",url,param)
		
	def pulsante1Premuto_a(self, evento):	### (3)
		print "Gestore di eventi 'pulsante1Premuto_a' (un involucro)"
		print self.e1.get(),self.e2.get(),self.e3.get(),self.cb3.get()
		print str(self.e1.get())
		self.send_init(str(self.e1.get()),self.e4.get(),self.e5.get(),self.cb3.get())
		self.thread = IlMioThread("AB120002", "passwordcassa",self.e3.get(),self.e2.get(),self.e1.get())
		self.thread.start()

	
	def send_stop(self,matricola):
		url = "v1/dispositivi/corrispettivi/stop/"
		self.send_get("localhost",url,matricola)
		
	def send_getinfo(self,matricola):
		url = "v1/dispositivi/corrispettivi/info/"
		self.send_get("localhost",url,matricola)


class IlMioThread (threading.Thread):
	def __init__(self, cassa, password,second,ip,matr):
		threading.Thread.__init__(self)
		self.cassauser = cassa
		self.password = password
		self.second = second
		self.set_ip_server = ip
		self.matricola = matr
	
	def createhash2(content):
		sha256 = hashlib.sha256()
		sha256.update(content)
		return base64.b64encode(sha256.digest())
	
	def dateplus(self,date,ora):
		text = str(date)+str(ora)
		datet = datetime.datetime.strptime(text, '%d%m%Y%H:%M:%S')
		end_date = datet + datetime.timedelta(days=1)
		return end_date.strftime('%d%m%Y')
	
	
	def dateminus(self,date,ora):
		text = str(date)+str(ora)
		datet = datetime.datetime.strptime(text, '%d%m%Y%H:%M:%S')
		end_date = datet - datetime.timedelta(days=1)
		return end_date.strftime('%d%m%Y')
	
	def send_post(self,content, url, user, password):
		print "https://"+self.set_ip_server+"/"+url
		base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
		print base64string
		pem = 'CASogeiTest.cer'
		#response = requests.post('https://'+self.set_ip_server+'/'+url,data=content,headers={"Content-Type": "application/xml", "Authorization": "BASIC %s" % base64string  }, verify=False)
		response = requests.post('https://'+self.set_ip_server+'/'+url,data=content,auth=HTTPBasicAuth(user, password),headers={"Content-Type": "application/xml"}, verify=False)
		print response.text
		assert response.status_code == 200
		return response.text
		
	def send_get(self,content, url):
		print "https://"+self.set_ip_server+"/"+url
		base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
		pem = 'CASogeiTest.cer'
		response = requests.get('https://'+self.set_ip_server+'/'+url,data=content,headers={"Content-Type": "application/xml", "Authorization": "BASIC %s" % base64string  }, verify=False)	
		print response.text
		assert response.status_code == 200
		return response.text
	
	def createhash(self,content):
		sha256 = hashlib.sha256()
		sha256.update(content)
		return sha256.hexdigest()
	
	def hmacsha256(self,key,mess):
		digest = hmac.new(bytes(key).encode('utf-8'), bytes(mess).encode('utf-8'), digestmod=hashlib.sha256).digest()
		signature = base64.b64encode(digest)
		return signature 
		
	
	def send_newpuntocassa_server(self,puntocassa,password):
		url = "ver1/api/configurazione/puntocassa"
		content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><ModificaMappa><TecnicoCF>AAABBB99C88D777E</TecnicoCF><LaboratorioPI>07123456789</LaboratorioPI><PuntoCassa>"+puntocassa+"</PuntoCassa><NuovoPuntoCassa/><Informazioni>Punto Cassa new</Informazioni></ModificaMappa>"
		self.send_post(content,url,puntocassa, password)
	
		
	def send_delpuntocassa_server(self,puntocassa,password):
		url = "ver1/api/configurazione/puntocassa"
		content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><ModificaMappa><TecnicoCF>AAABBB99C88D777E</TecnicoCF><LaboratorioPI>07123456789</LaboratorioPI><PuntoCassa>"+puntocassa+"</PuntoCassa><Rimuovi/><Informazioni>Punto Cassa new</Informazioni></ModificaMappa>"
		self.send_post(content,url,puntocassa,password)	
		
	def send_configurazione_serverURL(self,user,password):
		url = "ver1/api/configurazione/rete"
		content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><ConfigurazioneIP><URLAgenziaEntrate>https://192.168.1.146/v1/</URLAgenziaEntrate></ConfigurazioneIP>"
		send_post(content,url,user,password)

	def read_configurazione_serverURL(self,user,password):
		url = "ver1/api/richiesta/rete"
		content = ""
		send_get(content,url,user,password)
	
	def send_stato_server(self,user, password):
		url = "ServerRT/ver1/api/richiesta/stato/server"
		content = ""#"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura></Chiusura>"
		self.send_post(content,url,user, password)
	
	def send_stato_db(self,user, password):
		url = "ServerRT/ver1/api/richiesta/stato/db"
		content = ""#"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura></Chiusura>"
		self.send_post(content,url)
	
		
	def send_chiusura_cassa(self,user, password):
		url = "ver1/api/richiesta/chiusura"
		content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura></Chiusura>"
		self.send_post(content,url,user, password)
	
	def send_chiusura_server(self,user, password):
		url = "ServerRT/ver1/api/richiesta/chiusura"
		content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura><ServerRT/></Chiusura>"
		self.send_post(content,url,user, password)
		
	def send_forza_chiusura_server(self,user, password):
		url = "ServerRT/ver1/api/richiesta/chiusura"
		content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Chiusura><ForzaChiusura/></Chiusura>"
		self.send_post(content,url,user, password)	
		
	def send_apertura_cassa(self,user, password):
		url = "ServerRT/ver1/api/richiesta/apertura"
		content = "<AperturaPuntoCassa/>"
		res = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><ConfermaAperturaPuntoCassa><UltimaChiusura>0000</UltimaChiusura></ConfermaAperturaPuntoCassa>"
		response = self.send_post(content,url,user, password)
		mydoc = minidom.parseString(response)
		UltimaChiusura = mydoc.getElementsByTagName("UltimaChiusura")
		return UltimaChiusura[0].firstChild.data
	
	def send_ric_token_cassa(self,user, password):
		url = "ver1/api/richiesta/token"
		content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><RichiestaToken></RichiestaToken>"
		res = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><RestituzioneToken><Token>98C6F5255688BB32393033323031383030303130303030303030303030303030</Token><MatricolaRT>88S25000010</MatricolaRT><PuntoCassa>AB120001</PuntoCassa><DataOra><Data>29032018</Data><Ora>17:47:26</Ora></DataOra></RestituzioneToken>"
		response = self.send_post(content,url,user, password)
		mydoc = minidom.parseString(response)
		Tokens = mydoc.getElementsByTagName("Token")
		Datas = mydoc.getElementsByTagName("Data")
		Oras = mydoc.getElementsByTagName("Ora")
		matricolaread = mydoc.getElementsByTagName("MatricolaRT")
		if (not matricolaread[0].firstChild.data in self.matricola):
			print "matricola del server diversa da quella impostata"
			exit(0)
		print Datas[0].firstChild.data
		print Oras[0].firstChild.data
		return Tokens[0].firstChild.data,Datas[0].firstChild.data,Oras[0].firstChild.data
		
	def send_documento(self,scontrino,cdcp,tk,user, password):
		url = "ver1/api/invio/documento"
		content = "<?xmlversion=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Documento><CCDCPrecedente>"+cdcp+"</CCDCPrecedente><PuntoCassa>"+user+"</PuntoCassa>"+scontrino+"<CCDC>"+tk+"</CCDC></Documento>"
		#print content
		cc = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Documento><CCDCPrecedente>"+cdcp+"</CCDCPrecedente><PuntoCassa>"+user+"</PuntoCassa>"+scontrino+"<CCDC>"+tk+"</CCDC></Documento>"
		#res = "<?xmlversion=\"1.0\" encoding=\"UTF-8\"?><ConfermaDocumento><Data>29032018</Data><TotaleGiornaliero>12,20</TotaleGiornaliero><IdentificativoDocumento><NumeroAzzeramento>0001</NumeroAzzeramento><NumeroDocumento>0001</NumeroDocumento></IdentificativoDocumento></ConfermaDocumento>"
		print cc
		response = self.send_post(cc,url,user, password)
		mydoc = minidom.parseString(response)
		NumeroAzzeramentos = mydoc.getElementsByTagName("NumeroAzzeramento")
		NumeroDocumentos = mydoc.getElementsByTagName("NumeroDocumento")
		TotaleGiornalieros = mydoc.getElementsByTagName("TotaleGiornaliero")
		print NumeroAzzeramentos[0].firstChild.data
		print NumeroDocumentos[0].firstChild.data
		print TotaleGiornalieros[0].firstChild.data
	
	
	def crea_rettifica(self,chiusura,data,ora,tkold,ved,ndoc,referenceClosurenumber,referenceDocnumber,doctype,user, password):
		annullo = 1 #annullo
		if(doctype == 3):
			annullo = 0 #reso
		rettifica = "<RettificaScontrino><Data>"+data+"</Data><Ora>"+ora+"</Ora><NumeroDocumento>"+str(ndoc).zfill(4)+"</NumeroDocumento><NumeroAzzeramento>"+str(chiusura).zfill(4)+"</NumeroAzzeramento><RiferimentoDocumento><DataRegistrazione>"+data+"</DataRegistrazione><OrarioRegistrazione>"+ora+"</OrarioRegistrazione><NumeroProgressivo>"+str(referenceClosurenumber).zfill(4)+"-"+str(referenceDocnumber).zfill(4)+"</NumeroProgressivo></RiferimentoDocumento>"+ved+"<Annullamento>"+str(annullo)+"</Annullamento></RettificaScontrino>"
		cont = tkold+matricola+user+rettifica
		tk = self.createhash(cont)
		self.send_documento(rettifica,tkold,tk.upper(),user, password)
		return tk.upper()
	
	
	
	def read(self,filename):
		spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
		header = spamReader[0]
		del spamReader[0]
		return spamReader
	
	def readers(self,tok,data,ora,z,user, password):
		spamReader = self.read(sys.argv[1])
		nline = 0
		prev = {}
		prev2 = {}
		taxs = []
		amount = 0
		ndoc = 1
		print "#####"
		da = 0
		loop = 0
		max = len(spamReader)
		while da < max :
			line = spamReader[da]
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
			da +=1
			if('-' in rif ):
				rifsplit = rif.split("-")
				typ = rifsplit[0]
				rifDoc = rifsplit[1]
				referenceClosurenumber = z
				referenceDocnumber = int(rifDoc)+(loop*11)
				if(typ == "5"):
					doctype = 5
				if(typ == "3"):
					doctype = 3
			vendita1 = "<Dettagli><Vendita><Descrizione>Articolo1</Descrizione><Importo>"+importosenzasconto+"</Importo><Quantita>1</Quantita><PrezzoUnitario>"+importosenzasconto+"</PrezzoUnitario><CodiceIVA><Aliquota>"+aliquota+"</Aliquota></CodiceIVA></Vendita></Dettagli>"
			vendita2 = "<Dettagli><Vendita><Descrizione>Articolo2</Descrizione><Importo>"+importosenzasconto2+"</Importo><Quantita>1</Quantita><PrezzoUnitario>"+importosenzasconto2+"</PrezzoUnitario><CodiceIVA><Aliquota>"+aliquota2+"</Aliquota></CodiceIVA></Vendita></Dettagli>"
			if("E" in aliquota or "N" in aliquota or "R" in aliquota or "A" in aliquota    ):
				vendita1 = vendita1.replace("Aliquota","CodiceEsenzioneIVA",2)
			if("E" in aliquota2 or "N" in aliquota2 or "R" in aliquota2 or "A" in aliquota2    ):
				vendita2 = vendita2.replace("Aliquota","CodiceEsenzioneIVA",2)
			sconto1 = ""
			sconto2 = ""
			if float(valoresconto.replace(",","."))>0:
				sconto1 = "<Dettagli><ModificatoreSuArticolo><Descrizione>Sconto</Descrizione><Importo>"+valoresconto+"</Importo><Segno>-</Segno><CodiceIVA><Aliquota>"+aliquota+"</Aliquota></CodiceIVA></ModificatoreSuArticolo></Dettagli>"
				if("E" in aliquota or "N" in aliquota or "R" in aliquota or "A" in aliquota    ):
					sconto1 = sconto1.replace("Aliquota","CodiceEsenzioneIVA",2)
			if float(valoresconto2.replace(",","."))>0:
				sconto2 = "<Dettagli><ModificatoreSuArticolo><Descrizione>Sconto</Descrizione><Importo>"+valoresconto2+"</Importo><Segno>-</Segno><CodiceIVA><Aliquota>"+aliquota2+"</Aliquota></CodiceIVA></ModificatoreSuArticolo></Dettagli>"
				if("E" in aliquota2 or "N" in aliquota2 or "R" in aliquota2 or "A" in aliquota2 ):
					sconto2 = sconto2.replace("Aliquota","CodiceEsenzioneIVA",2)
			current = vendita1+sconto1
			current2 = vendita2+sconto2
			nline +=1
			if(tipodocumento!="TOTALE"):
				taxs = self.createTAX(importoscontato,imposta,aliquota,importoscontato2,imposta2,aliquota2,imponibile,imponibile2) 
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
				pagare = "<Dettagli><Pagamento><Descrizione>Contanti</Descrizione><Importo>"+pagementoC+"</Importo><Tipo>PC</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Elettronico</Descrizione><Importo>"+pagementoE+"</Importo><Tipo>PE</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Ticket</Descrizione><Importo>"+tk+"</Importo><Tipo>TK</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>NonRiscosso</Descrizione><Importo>"+pagementoCred+"</Importo><Tipo>NR</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Resto</Descrizione><Importo>"+resto+"</Importo><Tipo>RS</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Assegno</Descrizione><Importo>"+assegno+"</Importo><Tipo>AS</Tipo></Pagamento></Dettagli>"
				totale = "<Totale>"+line[1]+"</Totale>"
				#print doctype
				if(doctype==1):
					ved =  prev+prev2+pagare+totale+taxs
					newtk = self.creascontrino2(z,data,ora,tok,ved,ndoc,user, password)
				else:
					ved =  prev+prev2+totale+taxs
					newtk = self.crea_rettifica(z,data,ora,tok,ved,ndoc,referenceClosurenumber,referenceDocnumber,doctype,user, password)
				tok = newtk
				data = self.dateminus(data,ora)
				mod = ndoc % 11
				if(mod==0):
					da = 0
					loop =loop+1
				ndoc+=1
				#time.sleep(1)
			if (loop==4):
				break
	
	
	def createTAX(self,importoscontato,imposta,aliquota,importoscontato2,imposta2,aliquota2,imponibile,imponibile2):
		tax = ""
		if aliquota2!=aliquota:
			if("E" in aliquota or "N" in aliquota or "R" in aliquota or "A" in aliquota   ):
				imponibile = importoscontato
			if("E" in aliquota2 or "N" in aliquota2 or "R" in aliquota2 or "A" in aliquota2   ):
				imponibile2 = importoscontato2
			tax1 = "<CorrispettiviIVA><Importo>"+importoscontato+"</Importo><BaseImponibile>"+imponibile+"</BaseImponibile><Imposta>"+imposta+"</Imposta><CodiceIVA><Aliquota>"+aliquota+"</Aliquota></CodiceIVA></CorrispettiviIVA>"
			tax2 = "<CorrispettiviIVA><Importo>"+importoscontato2+"</Importo><BaseImponibile>"+imponibile2+"</BaseImponibile><Imposta>"+imposta2+"</Imposta><CodiceIVA><Aliquota>"+aliquota2+"</Aliquota></CodiceIVA></CorrispettiviIVA>"
			if("E" in aliquota or "N" in aliquota or "R" in aliquota or "A" in aliquota   ):
				tax1 = tax1.replace("Aliquota","CodiceEsenzioneIVA",2)
				tax1 = tax1.replace("<Imposta>0,00</Imposta>","")			
			if("E" in aliquota2 or "N" in aliquota2 or "R" in aliquota2 or "A" in aliquota2  ):
				tax2 = tax2.replace("Aliquota","CodiceEsenzioneIVA",2)
				tax2 = tax2.replace("<Imposta>0,00</Imposta>","")
			tax = tax1+tax2
		else:
			if("E" in aliquota or "N" in aliquota or "R" in aliquota or "A" in aliquota   ):
				imponibile = importoscontato
				imponibile2 = importoscontato2
			imp = float(importoscontato)
			impost = float(imposta)
			impo = float(imponibile)
			imp2 = float(importoscontato2)
			impost2 = float(imposta2)
			impo2 = float(imponibile2)
			
			tax = "<CorrispettiviIVA><Importo>"+(imp+imp2)+"</Importo><BaseImponibile>"+(impo+impo2)+"</BaseImponibile><Imposta>"+(impost+impost2)+"</Imposta><CodiceIVA><Aliquota>"+aliquota+"</Aliquota></CodiceIVA></CorrispettiviIVA>"
			if("E" in aliquota or "N" in aliquota or "R" in aliquota or "A" in aliquota   ):
				tax = tax.replace("Aliquota","CodiceEsenzioneIVA",2)
				tax = tax.replace("<Imposta>0,00</Imposta>","")
		return tax
	
	
	def creascontrino(self,chiusura,data,ora,tkold,user, password):
		scontrino = "<Scontrino><Data>"+data+"</Data><Ora>"+ora+"</Ora><NumeroDocumento>0001</NumeroDocumento><NumeroAzzeramento>"+str(chiusura).zfill(4)+"</NumeroAzzeramento><Dettagli><Vendita><Descrizione>Articolo16</Descrizione><Importo>10,00</Importo><Quantita>1</Quantita><PrezzoUnitario>10,00</PrezzoUnitario><CodiceIVA><Aliquota>10,00</Aliquota></CodiceIVA></Vendita></Dettagli><Dettagli><Pagamento><Descrizione>Contanti</Descrizione><Importo>10,00</Importo><Tipo>PC</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Elettronico</Descrizione><Importo>0,00</Importo><Tipo>PE</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Ticket</Descrizione><Importo>0,00</Importo><Tipo>TK</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>NonRiscosso</Descrizione><Importo>0,00</Importo><Tipo>NR</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Resto</Descrizione><Importo>0,00</Importo><Tipo>RS</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Assegno</Descrizione><Importo>0,00</Importo><Tipo>AS</Tipo></Pagamento></Dettagli><Totale>10,00</Totale><CorrispettiviIVA><Importo>10,00</Importo><BaseImponibile>9,09</BaseImponibile><Imposta>0,91</Imposta><CodiceIVA><Aliquota>10,00</Aliquota></CodiceIVA></CorrispettiviIVA></Scontrino>"
		cont = tkold+self.matricola+user+scontrino
		tk = self.createhash(cont)
		self.send_documento(scontrino,tkold,tk.upper(),user, password)
	
	def creascontrino2(self,chiusura,data,ora,tkold,ved,ndoc,user, password):
		scontrino = "<Scontrino><Data>"+data+"</Data><Ora>"+ora+"</Ora><NumeroDocumento>"+str(ndoc).zfill(4)+"</NumeroDocumento><NumeroAzzeramento>"+str(chiusura).zfill(4)+"</NumeroAzzeramento>"+ved+"</Scontrino>"
		cont = tkold+matricola+user+scontrino
		tk = self.createhash(cont)
		self.send_documento(scontrino,tkold,tk.upper(),user, password)
		return tk.upper()
	
		
	def creacassastart(self,cassa,password):
		self.send_newpuntocassa_server(cassa,password)
		self.testFW(cassa,password)
		
		
	def loop_HW(self,user,password,second):
		self.send_chiusura_cassa(user, password)
		while True:
			kiusura = self.send_apertura_cassa(user, password)
			z = str(int(kiusura)+1)
			#print str(kiu)
			#exit(0)
			tokenp = self.send_ric_token_cassa(user, password)
			self.creascontrino(z,tokenp[1],tokenp[2],tokenp[0],user, password)
			self.send_chiusura_cassa(user, password)	
			self.send_chiusura_server(user, password)	
			time.sleep(float(second))
		
	
		
		
	def testFW(self,user,password):
		self.send_chiusura_cassa(user, password)
		tokenp = self.send_ric_token_cassa(user, password)
		kiusura = self.send_apertura_cassa(user, password)
		time.sleep(2)
		z = str(int(kiusura)+1)
		ved = self.readers(tokenp[0],tokenp[1],tokenp[2],z,user, password)
		self.send_chiusura_cassa(user, password)
		#self.send_chiusura_server(user, password)
		
	def run(self):
		self.loop_HW(self.cassauser,self.password,self.second)
		#self.creacassastart(self.cassauser,self.password)
		
		
radice = Tk()
#radice.geometry('{}x{}'.format(460, 350))
miaApp = MiaApp(radice)
radice.mainloop()