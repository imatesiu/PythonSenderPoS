#!/usr/bin/python
import socket 
import time

def conn(ip,port):
	opened_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket.connect((ip, port))
	return opened_socket

def send(msg):
	print msg
	res = opened_socket.send(msg.upper())
	print res
	data = opened_socket.recv(2048).encode('hex')
	print data
	
def calculatecrc(msg):	
	init = '02'
	final = '03'
	cks = 0
	stringa = ''
	for elem in msg:
		cks += ord(elem)
	cks = (cks & 255) % 100
	stringa = msg + str(cks)
	#print stringa
	outHex = '02'
	for element in stringa:
		outHex += hex(ord(element))
	return (outHex + '03').replace("0x","").upper()
		

def send2(msg):
  try:
	opened_socket2 = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket2.connect((ip, port))
	print msg
	opened_socket2.send(msg)
	data = opened_socket2.recv(1024).encode('hex')
	print data
	opened_socket2.close()
  except Exception as e:
  	print str(e)



ip = "192.168.1.206"
port =9103 	


#opened_socket  = conn(ip,port)


k=147

i = 1 
for cicli in range(1,3):
	si = '02332f532f2532322042454e452f2f312f312f312f2f2f302f302f363503' #'3/S/%22 BENE//1/1/1///0/0/'

	send2(si.decode('hex'))
	
	si= '02352f312f302f333503' # '5/1/0'
	send2(si.decode('hex'))
	time.sleep(2)
	si = '02782f372f313303'#'x/7'
	send2(si.decode('hex'))
	si = '02282f383703'
	send2(si.decode('hex'))
	
exit(0)

