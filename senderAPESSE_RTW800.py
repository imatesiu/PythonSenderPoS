#!/usr/bin/python
import socket 
import time

def conn(ip,port):
	opened_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket.connect((ip, port))
	return opened_socket

def send(msg):
	print msg
	res = opened_socket.send(msg)
	print res
	

#opened_socket = conn(ip,port)	
	
ip = "146.48.84.154"
port =9101

def send2(msg):
  try:
	opened_socket2 = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket2.connect((ip, port))
	print msg
	opened_socket2.send(msg)
	data = opened_socket2.recv(1024).decode()
	print data
	opened_socket2.close()
  except Exception as e:
  	print str(e)

k=147

Url1 = "\/80/////////////v-apid-ivaservizi.agenziaentrate.gov.it~v1~dispositivi/v-apid-ivaservizi.agenziaentrate.gov.it~v1~dispositivi/////////"

Urllocale = "\/80/////////////192.168.1.146~v1~dispositivi/192.168.1.146~v1~dispositivi/////////"
Urllocale2 = "\/80/////////////sseapid.isti.cnr.it~v1~dispositivi/sseapid.isti.cnr.it~v1~dispositivi/////////"

#Lotteria
#
z = 29
ndoc = 1
date = "17052022"
Matricola = ""
#reso
i = 1 
for cicli in range(1,98):
	
	#send2(Urllocale2)
	#print Urllocale 
	send2('I/12345678/0')
	send2('3/S/CODA A//1.0/10.0/1/////')
	send2('5/5/0.00//27022024123400123454///')
	#send2('x/7')
	#send2(',/80')
	
	i+=1
	print cicli
	time.sleep(5)
	
exit(0)

