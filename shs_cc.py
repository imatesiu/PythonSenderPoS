#!/usr/bin/python
import socket 
import time

def send(msg,ip,port):
	opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	opened_socket.sendto(msg, (ip, port))
	
	
	
ip = "192.168.1.2"
port = 3001

#messaggio = "\"ciao\"@"
#messaggio = "J"
onetoten = range(1,8)
for count in onetoten:
	messaggio = "1F"
	send(messaggio,ip,port)

	#messaggio = "\"12345678\"53F"
	#send(messaggio,ip,port)
	#messaggio = "2T"
	#send(messaggio,ip,port)
	#messaggio = "2000H2T"
	#send(messaggio,ip,port)
	#print "2"
	#messaggio = "2000H3T"
	#send(messaggio,ip,port)
	#print "3"
	#messaggio = "2000H4T"
	#send(messaggio,ip,port)
	#print "4"
	#messaggio = "2000H5T"
	#send(messaggio,ip,port)
	#print "5"
	#messaggio = "2000H6T"
	#send(messaggio,ip,port)
	#print "6"
	#messaggio = "2000H1T"
	#send(messaggio,ip,port)
	#print "1"
	time.sleep(5)


exit(0)


