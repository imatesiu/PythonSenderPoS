#!/usr/bin/python
import sys
import urllib2, base64
import ssl
import requests
import time
from base64 import b64encode
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree
from datetime import timedelta
import xml.etree.ElementTree as ET
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
		v.set("80I15000026")
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

	def xmltodate(self, xml):
		root = ET.fromstring(xml)
		a = (root.findall(".//extraInfo"))
		text = a[0].text
		datet = datetime.strptime(text, '%d%m%Y%H%M%S')
		return datet
		#print res

	def dateplus(self, date):
		end_date = date + timedelta(days=1)
		return end_date.strftime('%d%m%Y')


	def createnewdata(self, xml):
		da = self.xmltodate(xml)
		r = self.dateplus(da)
		print r
		data4 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><SetEcrDate><SETDATE><DATE>"+r+"</DATE><TIME>010000</TIME></SETDATE></SetEcrDate></soap:Body></soap:Envelope>"
		return data4

	def send_post(self, content, set_ip_apparato):
		response = requests.post('http://'+set_ip_apparato+':80/oli_webservice.cgi',data=content,headers={"Content-Type": "text/xml"})
		print response.text
		assert response.status_code == 200
		return response.text

	def send_documentocommerciale(self, set_ip_apparato):
		documentocommerciale = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD>...<E_SALE>..<OPTYPE>1</OPTYPE>....<BARCODETYPE></BARCODETYPE>..<NUMBER>1</NUMBER>..<LISTPRICE>1</LISTPRICE>..<SALETYPE>1</SALETYPE>..<DESCRIPTION></DESCRIPTION>..<AMOUNT>1</AMOUNT>..<QUANTITY_1></QUANTITY_1>..<QUANTITY_2></QUANTITY_2>..<QUANTITY_3></QUANTITY_3>..<QUANTITY_4></QUANTITY_4>..<M_QUANTITY></M_QUANTITY>..<S_QUANTITY></S_QUANTITY>..<RAEETYPE></RAEETYPE>..<RAEEVALUE></RAEEVALUE>.</E_SALE></CMD><CMD>...<E_PAYMENT>..<P_TYPE>1</P_TYPE>...<NUMBER>1</NUMBER>...<DESCRIPTION>PAGAMENTO</DESCRIPTION>...<AMOUNT></AMOUNT>....<CUSTOMERACCOUNT></CUSTOMERACCOUNT>...</E_PAYMENT></CMD></EcrTickets></soap:Body></soap:Envelope>"
		self.send_post(documentocommerciale,set_ip_apparato)

	def send_zfiscale(self, set_ip_apparato):
		zfiscale = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><ExecuteReport>.<PRINTREP>1</PRINTREP>.<REPTYPE>1</REPTYPE>.<REPNUM>10</REPNUM>.</ExecuteReport></soap:Body></soap:Envelope>"
		self.send_post(zfiscale,set_ip_apparato)

	def send_changedata(self, xml, set_ip_apparato):
		response = self.send_post(xml,set_ip_apparato)
		return response

	def create_send_new_data(self,  set_ip_apparato):
		changedate = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD><GETDATE></GETDATE></CMD></EcrTickets></soap:Body></soap:Envelope>"
		xml = self.send_changedata(changedate,set_ip_apparato)
		d = str(xml)
		dmsg = self.createnewdata(d)
		self.send_post(dmsg,set_ip_apparato)
		self.send_post(dmsg,set_ip_apparato)

	def loop_HW(self,user,password,second):
		num = 0
		while not self.dead:
			if num == 1 or num == 40:
					self.create_send_new_data(self.set_ip_server)
					num = 2
			self.send_documentocommerciale(self.set_ip_server)
			self.send_zfiscale(self.set_ip_server)
			time.sleep(float(second))
			while(self.pause):
				time.sleep(5)




	def run(self):
		self.loop_HW(self.cassauser,self.password,self.second)
		#self.creacassastart(self.cassauser,self.password)




#radice.geometry('{}x{}'.format(460, 350))
miaApp = MiaApp(radice)
radice.mainloop()
