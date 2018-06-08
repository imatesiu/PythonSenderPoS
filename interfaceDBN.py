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
from requests.exceptions import ConnectionError
from PIL import Image, ImageTk
import tkMessageBox

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


ip_server_rt = "localhost"
admin_user = "admin"
admin_password = "RCH"
radice = Tk()
pil_image = Image.open("CNR.png")

#get the size of the original image
width_org, height_org = pil_image.size
factor = 0.15
width = int(width_org * factor)
height = int(height_org * factor)
pil_image2 = pil_image.resize((width, height), Image.ANTIALIAS)
tk_image = ImageTk.PhotoImage(pil_image2)

class MiaApp:


		
		
	def __init__(self, genitore):

		
		
		self.mioGenitore = genitore
		self.mioContenitore1 = Frame(genitore)
		genitore.title("Python RCH Sender")
		genitore.iconbitmap(r'favicon.ico')
		
		Label(self.mioContenitore1, text="Matricola: ").grid(row=0,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="IP del RT: ").grid(row=1,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="Intervallo: ").grid(row=2,pady=5,sticky=W)
		v = StringVar()
		v.set("88S25000026")
		self.e1 = Entry(self.mioContenitore1,textvariable=v)
		v1 = StringVar()
		v1.set("192.168.1.11")#192.168.1.146
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
		
		self.prove = ("Termiche","Impermeabilita","Vibrazione","ImmunitaScaricheElettrostaticheESD","ImmunitaCampoElettromagneticoRadiofrequenza","ImmunitaTransitoriVelociEFTBURST","ImmunitaImpulsiSURGE","ImmunitaDisturbiCondottiContinuiRadiofrequenza","ImmunitaCampiMagneticiFrequenzaRete","ImmunitaBuchiInterruzioniTensione","VariazioniTensione","ProvaDurataBatteria","BatteriaSottoProtezioneSF","AlimentazioneBatteriaSenzaVincoloFiscale","Guastoemalfunzionamento")
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



		imglabel = Button(self.mioContenitore1, image=tk_image, command = self.pulsanteCNR)
		imglabel.grid(row=9,column=1) 
		#imglabel.pack()
		self.mioContenitore1.pack()


	def pulsanteCNR(self):
		tkMessageBox.showinfo("Fiscal Group", "ISTI CNR SSEC Fiscal Group")


	def pulsante1Premuto(self):	### (2)
		print "Gestore di eventi 'pulsante1Premuto'"
		#if self.pulsante1["background"] == "green":
		#	self.pulsante1["background"] = "yellow"
		#else:
		#	self.pulsante1["background"] = "green"

	def pulsante2Premuto(self):	### (2)
		try:
			if self.pulsante2["background"] == "yellow":
				self.pulsante2["background"] = "green"
				print "Gestore di eventi pulsante Pausa Premuto - Pausa TRUE"
				self.thread.pause = True
			else:
				self.pulsante2["background"] = "yellow"
				print "Gestore di eventi pulsante Pausa Premuto - Pausa FALSE"
				self.thread.pause = False
		except AttributeError: print "Ops"

	def pulsante3Premuto(self):	### (2)
		print "Gestore di eventi pulsante Stop Premuto"
		self.send_stop(str(self.e1.get()))
		try:
			self.thread.pause = False
			self.thread.dead = True
		except AttributeError: print "Ops"
		#self.mioGenitore.destroy()
		
		
	def pulsanteEPremuto_a(self, evento):	### (3)
		print "Gestore di eventi 'pulsante2Premuto_a' (un involucro)"

		
	def pulsanteInfoPremuto(self):	### (3)
		print "Gestore di eventi pulsante Info Premuto"
		self.send_getinfo(str(self.e1.get()))
		
		
	def pulsanteEPremuto(self):	### (3)
		print "Gestore di eventi pulsante Exit Premuto"
		try:
			self.thread.dead = True
			self.thread.pause = False
		except AttributeError: print "Ops"
		exit(0)
		
		
	def send_get(self,ip_server, url, param):
		print "https://"+ip_server+"/"+url+param
		try:
			#base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
			#pem = 'CASogeiTest.cer'
			response = requests.get('http://'+ip_server+':9090/'+url+param,headers={"Content-Type": "application/xml"}, verify=False)
			print response.text
			assert response.status_code == 200
			return response.text
		except ConnectionError: print "Problemi di Rete"
		
		
	def send_init(self,matricola,gt,z,prova):
		#https://localhost/v1/dispositivi/corrispettivi/init/80M08002493?grantot=28.8&desc=Termiche&z=33
		url = "v1/dispositivi/corrispettivi/init/"
		param = matricola+"?grantot="+gt+"&desc="+prova+"&z="+z
		self.send_get(ip_server_rt,url,param)
		
	def pulsante1Premuto_a(self, evento):	### (3)
		print "Gestore di eventi pulsante Start Premuto"
		gt = self.e4.get()
		gt = gt.replace(",",".")
		self.send_init(str(self.e1.get()),gt,self.e5.get(),self.cb3.get())
		self.thread = IlMioThread("AB120002", "aaa",self.e3.get(),self.e2.get(),self.e1.get())
		self.thread.start()

	
	def send_stop(self,matricola):
		url = "v1/dispositivi/corrispettivi/stop/"
		self.send_get(ip_server_rt,url,matricola)
		
	def send_getinfo(self,matricola):
		url = "v1/dispositivi/corrispettivi/info/"
		self.send_get(ip_server_rt,url,matricola)


class IlMioThread (threading.Thread):
	def __init__(self, cassa, password,second,ip,matr):
		threading.Thread.__init__(self)
		self.cassauser = cassa
		self.password = password
		self.second = second
		self.set_ip_server = ip
		self.matricola = matr
		self.dead = False
		self.pause = False
	
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
		

	def createhash(self,content):
		sha256 = hashlib.sha256()
		sha256.update(content)
		return sha256.hexdigest()
	


		
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
		
	def send_configurazione_serverURL(self):
		url = "ver1/api/configurazione/rete"
		content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><ConfigurazioneIP><URLAgenziaEntrate>https://192.168.1.146/v1/</URLAgenziaEntrate></ConfigurazioneIP>"
		self.send_post(content, url, admin_user,admin_password)
		
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
	
	
	
	def creascontrino(self,chiusura,data,ora,tkold,user, password):
		scontrino = "<Scontrino><Data>"+data+"</Data><Ora>"+ora+"</Ora><NumeroDocumento>0001</NumeroDocumento><NumeroAzzeramento>"+str(chiusura).zfill(4)+"</NumeroAzzeramento><Dettagli><Vendita><Descrizione>Articolo16</Descrizione><Importo>10,00</Importo><Quantita>1</Quantita><PrezzoUnitario>10,00</PrezzoUnitario><CodiceIVA><Aliquota>10,00</Aliquota></CodiceIVA></Vendita></Dettagli><Dettagli><Pagamento><Descrizione>Contanti</Descrizione><Importo>10,00</Importo><Tipo>PC</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Elettronico</Descrizione><Importo>0,00</Importo><Tipo>PE</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Ticket</Descrizione><Importo>0,00</Importo><Tipo>TK</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>NonRiscosso</Descrizione><Importo>0,00</Importo><Tipo>NR</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Resto</Descrizione><Importo>0,00</Importo><Tipo>RS</Tipo></Pagamento></Dettagli><Dettagli><Pagamento><Descrizione>Assegno</Descrizione><Importo>0,00</Importo><Tipo>AS</Tipo></Pagamento></Dettagli><Totale>10,00</Totale><CorrispettiviIVA><Importo>10,00</Importo><BaseImponibile>9,09</BaseImponibile><Imposta>0,91</Imposta><CodiceIVA><Aliquota>10,00</Aliquota></CodiceIVA></CorrispettiviIVA></Scontrino>"
		cont = tkold+self.matricola+user+scontrino
		tk = self.createhash(cont)
		self.send_documento(scontrino,tkold,tk.upper(),user, password)
	

		
	def loop_HW(self,user,password,second):
		self.send_configurazione_serverURL();
		self.send_chiusura_cassa(user, password)
		while not self.dead:
			kiusura = self.send_apertura_cassa(user, password)
			z = str(int(kiusura)+1)
			#print str(kiu)
			#exit(0)
			tokenp = self.send_ric_token_cassa(user, password)
			self.creascontrino(z,tokenp[1],tokenp[2],tokenp[0],user, password)
			self.send_chiusura_cassa(user, password)	
			self.send_chiusura_server(user, password)	
			time.sleep(float(second))
			while(self.pause):
				time.sleep(5)
		



	def run(self):
		self.loop_HW(self.cassauser,self.password,self.second)
		#self.creacassastart(self.cassauser,self.password)
		



#radice.geometry('{}x{}'.format(460, 350))
miaApp = MiaApp(radice)
radice.mainloop()