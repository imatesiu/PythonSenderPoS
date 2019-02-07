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
import subprocess

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
admin_password = "admin"
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
		self.proc = None
		self.mioContenitore1 = Frame(genitore)
		genitore.title("Python EPSon Sender")
		genitore.iconbitmap(r'favicon.ico')
		
		Label(self.mioContenitore1, text="Matricola: ").grid(row=0,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="IP del RT: ").grid(row=1,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="Intervallo: ").grid(row=2,pady=5,sticky=W)
		v = StringVar()
		v.set("99SMM000989")
		self.e1 = Entry(self.mioContenitore1,textvariable=v)
		v1 = StringVar()
		v1.set("192.168.1.136")#192.168.1.146
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
			else:
				self.pulsante2["background"] = "yellow"
				print "Gestore di eventi pulsante Pausa Premuto - Pausa FALSE"
		except AttributeError: print "Ops"

	def pulsante3Premuto(self):	### (2)
		print "Gestore di eventi pulsante Stop Premuto"
		self.send_stop(str(self.e1.get()))
		if(self.proc!=None):
			self.proc.kill()
		self.proc=None
		#self.mioGenitore.destroy()
		
		
	def pulsanteEPremuto_a(self, evento):	### (3)
		print "Gestore di eventi 'pulsante2Premuto_a' (un involucro)"

		
	def pulsanteInfoPremuto(self):	### (3)
		print "Gestore di eventi pulsante Info Premuto"
		self.send_getinfo(str(self.e1.get()))
		
		
	def pulsanteEPremuto(self):	### (3)
		print "Gestore di eventi pulsante Exit Premuto"
		if(self.proc!=None):
			self.proc.kill()
		self.proc=None
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
		if(self.proc==None):
			self.proc = subprocess.Popen("python stress-test.py", shell=True)


	
	def send_stop(self,matricola):
		url = "v1/dispositivi/corrispettivi/stop/"
		self.send_get(ip_server_rt,url,matricola)
		
	def send_getinfo(self,matricola):
		url = "v1/dispositivi/corrispettivi/info/"
		self.send_get(ip_server_rt,url,matricola)


	



#radice.geometry('{}x{}'.format(460, 350))
miaApp = MiaApp(radice)
radice.mainloop()