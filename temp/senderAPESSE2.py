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
	
ip = "192.168.1.169"
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


Url1 = "\/80/////////////v-apid-ivaservizi.agenziaentrate.gov.it/v-apid-ivaservizi.agenziaentrate.gov.it/////////"

Urllocale = "\/80/////////////192.168.1.146/192.168.1.146/////////"
Urllocale2 = "\/80/////////////sseapid.isti.cnr.it/sseapid.isti.cnr.it/////////"



#Lotteria
#
z = 200
ndoc = 1
date = "17052022"
Matricola = ""
#reso
i = 1 
for cicli in range(1,150):
	#send2(Urllocale)
	#exit(0)
	#send2('I/123456789/0/')
	#send2('3/S/test_01//1/20.0/1//')
	send2('3/S/test_01//1/20.0/1//')
	time.sleep(2)
	#send2('I/12345678/0/')
	send2('5/1/20.00////')
	time.sleep(2)
	send2('x/7/1/3////')
	print cicli
	time.sleep(20)
	
#time.sleep(50)
	
exit(0)

