#!/usr/bin/python
import socket 
import time

def conn(ip,port):
	opened_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket.connect((ip, port))
	return opened_socket



def send(msg,opened_socket):
	opened_socket.sendall(msg)
	#data = opened_socket.recv(1024)
	#print data
	
	
ip = "192.168.1.223"
port =1126

opened_socket = conn(ip,port)

#messaggio = "\"ciao\"@"
#messaggio = "J"
onetoten = range(1,600)
for count in onetoten:
	#messaggio = "2X"
	#send(messaggio,opened_socket)
	messaggio = "1000H1R"
	send(messaggio,opened_socket)
	#messaggio = "\"1234\"L"
	#send(messaggio,opened_socket)
	messaggio = "1T"
	send(messaggio,opened_socket)
	messaggio = "1F"
	send(messaggio,opened_socket)
	#time.sleep(2)
	#messaggio = "K"
	#send(messaggio,opened_socket)
	#messaggio = "K"
	#send(messaggio,opened_socket)
		
	print count
	time.sleep(240)
	#messaggio = "K"
	#send(messaggio,opened_socket)
	
exit(0)

'''
il comando  xxHnV, con xx importo gi pagato e n IVA di riferiemnto
Ad esempio:

10H1R 5H1V 1T

vendi 10 cent a reparto 1
di cui acconto 5 cent
chiudi contante


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
