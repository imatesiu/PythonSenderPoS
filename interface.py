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

from Tkinter import *
from ttk import Combobox

class MiaApp:


		
		
	def __init__(self, genitore):

		
		
		self.mioGenitore = genitore
		self.mioContenitore1 = Frame(genitore)
		self.mioContenitore1.pack()
		
		Label(self.mioContenitore1, text="Matricola: ").grid(row=0,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="Sent to IP: ").grid(row=1,column=0,pady=5,sticky=W)
		
		Label(self.mioContenitore1, text="Intervallo: ").grid(row=2,pady=5,sticky=W)
		
		self.e1 = Entry(self.mioContenitore1)
		self.e2 = Entry(self.mioContenitore1)
		self.e3 = Entry(self.mioContenitore1)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)

		
		self.prove = ("Termiche","Impermeabilita","Vibrazione","DisturbiElettromagnetici","DisturbiCondotti","BatteriaSottoProtezioneSF","AlimentazioneBatteriaSenzaVincoloFiscale","ScaricheElettrostatiche","Guastoemalfunzionamento")
		self.cbp3 = Label(self.mioContenitore1, text='Prova: ')
		self.cbp3.grid(row=3, column=0,pady=5)
		self.cb3 = Combobox(self.mioContenitore1, values=self.prove, state='readonly')
		self.cb3.current(1)  # set selection
		self.cb3.grid(row=3, column=1)

		
		self.pulsante1 = Button(self.mioContenitore1,
														command = self.pulsante1Premuto)
		self.pulsante1.bind("<Return>", self.pulsante1Premuto_a)	### (1)
		self.pulsante1.configure(text = "Start", background = "green")
		self.pulsante1.grid(row=4, column=0,pady=25)
		self.pulsante1.focus_force()
		
		
		self.pulsante2 = Button(self.mioContenitore1,
														command = self.pulsante2Premuto)
		self.pulsante2.bind("<Return>", self.pulsante2Premuto)	### (1)
		self.pulsante2.configure(text = "Pause", background = "yellow")
		self.pulsante2.grid(row=4, column=1)
		self.pulsante2.focus_force()
		
		self.pulsante3 = Button(self.mioContenitore1,
														command = self.pulsante3Premuto)
		self.pulsante3.bind("<Return>", self.pulsante3Premuto)	### (1)
		self.pulsante3.configure(text = "Stop", background = "red")
		self.pulsante3.grid(row=4, column=2)
		self.pulsante3.focus_force()
		
		

		self.pulsantee = Button(self.mioContenitore1,
														command = self.pulsanteEPremuto)
		self.pulsantee.bind("<Return>", self.pulsanteEPremuto_a)	### (1)
		self.pulsantee.configure(text = "Chiudi", background = "red")
		self.pulsantee.grid(row=6, column=0)
		
		self.pulsanteinfo = Button(self.mioContenitore1,
														command = self.pulsanteInfoPremuto)
		self.pulsanteinfo.bind("<Return>", self.pulsanteInfoPremuto)	### (1)
		self.pulsanteinfo.configure(text = "Info", background = "green")
		self.pulsanteinfo.grid(row=6, column=2)
		self.pulsanteinfo.focus_force()
		

		def apply(self):
			first = int(self.e1.get())
			second = int(self.e2.get())
			print first, second # or something

	def pulsante1Premuto(self):	### (2)
		print "Gestore di eventi 'pulsante1Premuto'"
		if self.pulsante1["background"] == "green":
			self.pulsante1["background"] = "yellow"
		else:
			self.pulsante1["background"] = "green"

	def pulsante2Premuto(self):	### (2)
		print "Gestore di eventi 'pulsante2Premuto'"
		self.mioGenitore.destroy()

	def pulsante3Premuto(self):	### (2)
		print "Gestore di eventi 'pulsante2Premuto'"
		self.mioGenitore.destroy()
				
		
	def pulsante2Premuto(self):	### (2)
		print "Gestore di eventi 'pulsante2Premuto'"
		self.mioGenitore.destroy()

	def pulsante1Premuto_a(self, evento):	### (3)
		print "Gestore di eventi 'pulsante1Premuto_a' (un involucro)"
		self.pulsante1Premuto()

	def pulsanteEPremuto_a(self, evento):	### (3)
		print "Gestore di eventi 'pulsante2Premuto_a' (un involucro)"
		self.pulsante2Premuto()
		
	def pulsanteInfoPremuto(self):	### (3)
		print "Gestore di eventi 'pulsante2Premuto_a' (un involucro)"
		self.pulsante2Premuto()
		
	def pulsanteEPremuto(self):	### (3)
		print "Gestore di eventi 'pulsante2Premuto_a' (un involucro)"
		self.pulsante2Premuto()


radice = Tk()
#radice.geometry('{}x{}'.format(460, 350))
miaApp = MiaApp(radice)
radice.mainloop()