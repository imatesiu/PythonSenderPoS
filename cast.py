#!/usr/bin/python
import socket 
import time,sys

def conn(ip,port):
	opened_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket.connect((ip, port))
	return opened_socket

def send(msg):
	print msg
	opened_socket.send(msg)
	#data = opened_socket.recv(1024)
	#opened_socket.close()
	#print data
	
	
ip = "192.168.1.5"
#cash port =1126
port =9150 #go

'''
1T    CONTANTI
2T    ASSEGNI
3T    CARTA CREDITO
4T    NON PAGATO CREDITO
5T    TICKET
6T   NON RISCOSSO SERVIZI
7T    SEGUIRa FATTURA
8T    NON RISCOSSO SSN
n9T  BUONO MONOUSO(n is vat)
10T  BUONO MULTIUSO
11T  SCONTO A PAGARE
12T  BUONO CELIACHIA
'''

znum = 2

if(len(sys.argv)>2):
	 ip = sys.argv[1]
	 znum = sys.argv[2]
	 
print ip
print znum
opened_socket = conn(ip,port)

onetoten = range(1,2)
for count in onetoten:
	messaggio = "K"
	send(messaggio)
	messaggio = "3348H1R 2000H1R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "2000H19T  1T"
	send(messaggio)
	time.sleep(1)
	send("1F")
exit(0)
time.sleep(2)
onetoten = range(1,16)
doc=1
for count in onetoten:

	
	
	messaggio = "\""+str(znum).zfill(4)+"-"+str(doc).zfill(4)+"-27092020\"105M"
	send(messaggio)
	doc +=1

	time.sleep(1)

time.sleep(15)
doc=6
for count in onetoten:

	
	
	messaggio = "\""+str(znum).zfill(4)+"-"+str(doc).zfill(4)+"-27092020\"105M"
	send(messaggio)
	doc +=1

	time.sleep(1)
exit(0)