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
	
ip = "192.168.1.45"
port =9100

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
for cicli in range(1,2):
    s = '023531303330303131313541727469636f6c6f20697661203232303030303030313030343303'
    invia  =  s.decode('hex')
    send2(invia)
    s = '0235323033303033343903'
    invia  =  s.decode('hex')
    send2(invia)
    s = '0235333033303131343903'
    invia  =  s.decode('hex')
    send2(invia)
    s = '0235343033303133353203'
    invia  =  s.decode('hex')
    send2(invia)
    s = '0235353032303032353003'
    invia  =  s.decode('hex')
    send2(invia)
    

exit(0)
