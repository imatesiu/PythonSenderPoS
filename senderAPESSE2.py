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
	
ip = "192.168.1.14"
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


#Lotteria
#
z = 29
ndoc = 1
date = "17052022"
Matricola = ""
#reso
i = 1 
for cicli in range(1,102):
	
	#send2('I/123456789/0/')
	send2('3/S/test_01//1/20.0/1//')
	#send2('3/S/test_01//1/20.0/1//')
	#send2('I/12345678/0/')
	send2('5/4/0.00////')
        send2('x/7/1/3////')
	i+=1
	print cicli
	time.sleep(10)
	
exit(0)

