#!/usr/bin/python
import socket 
import time

def conn(ip,port):
	opened_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket.connect((ip, port))
	return opened_socket

def send(msg,opened_socket):
	opened_socket.sendall(msg)
	
	
ip = "192.168.1.22"
port =1126

opened_socket = conn(ip,port)

#messaggio = "\"ciao\"@"
#messaggio = "J"
onetoten = range(1,3)
for count in onetoten:
	messaggio = "9000H1R"
	send(messaggio,opened_socket)
	messaggio = "1T"
	send(messaggio,opened_socket)
	messaggio = "1F"
	send(messaggio,opened_socket)
	print onetoten
	time.sleep(15)

exit(0)