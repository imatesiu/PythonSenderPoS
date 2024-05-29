#!/usr/bin/python
import socket 
import time

def conn(ip,port):
	opened_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket.connect((ip, port))
	return opened_socket

def send(msg):
	print msg
	opened_socket = conn(ip,port)
	res = opened_socket.sendall(msg)
	opened_socket.close()
	print res
	
	
ip = "192.168.1.51"
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



#messaggio = "\"ciao\"@"
#messaggio = "J"
'''
doc = 1
k = 5
onetoten = range(1,2)
for count in onetoten:
	print count
	#messaggio = "K"
	#send(messaggio,opened_socket)
	
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "15000H3R 5000H3V 12201H2R 2404H1R 2000H7R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "2200H6T 1T"
	send(messaggio,opened_socket)
	#messaggio = "12000H1T"
	time.sleep(2)
	exit(0)
	
	#messaggio = "K"
	#send(messaggio,opened_socket)	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "13322H2R 3300H2V 3300H21R 3789H1R 2456H10R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "700H2T 1000H10T  15000H1T"
	send(messaggio,opened_socket)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "3500H7R  8056H2R 6654H4R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "7T"
	send(messaggio,opened_socket)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "2817H8R 3889H1R 6700H3R 1300H4R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "1000H89T 15000H1T"
	send(messaggio,opened_socket)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "2889H6R 8888H9R 2200H23R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "10000H8T 1T"
	send(messaggio,opened_socket)

	time.sleep(2)
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "3800H1R 1333H3R 2000H23R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "1000H5T 5200H1T"
	send(messaggio,opened_socket)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "2346H1R 2000H23R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "1500H10T 2400H1T"
	send(messaggio,opened_socket)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "3345H1R 2000H21R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "1000H12T 3000H1T"
	send(messaggio,opened_socket)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	print messaggio
	send(messaggio,opened_socket)
	messaggio = "3346H1R 2000H1R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "2000H19T  1T"
	send(messaggio,opened_socket)
	

	#send(messaggio,opened_socket)
	#messaggio = "1F"
	#send(messaggio,opened_socket)
	#messaggio = "K"
	#send(messaggio,opened_socket)

	print count
	time.sleep(1)

exit(0) 


doc = 1
onetoten = range(1,10)
for count in onetoten:
	messaggio = "K"
	send(messaggio,opened_socket)
	''' '''
	
	
	messaggio = "\"0125-"+str(doc).zfill(4)+"-10082020\"105M"
	print messaggio
	send(messaggio,opened_socket)
	doc +=1

	#send(messaggio,opened_socket)
	#messaggio = "1F"
	#send(messaggio,opened_socket)
	#messaggio = "K"
	#send(messaggio,opened_socket)

	print count
	time.sleep(1)

exit(0)
'''
onetoten = range(1,2)
for count in onetoten:
	#messaggio = "K"
	#send(messaggio,opened_socket)
	''' '''
	messaggio = "15000H3R 5000H3V 12201H2R 2404H1R 2000H7R"
	#send(messaggio,opened_socket)
	time.sleep(100)
	messaggio = "\"1234\"L"
	#send(messaggio)
	time.sleep(100)
	messaggio = "2200H6T 700H2T  12000H3T 11705H1T"
	#send(messaggio)
	time.sleep(100)
	messaggio = "13322H2R 3300H2V 3300H21R 3789H1R 2456H10R"
	#send(messaggio)
	messaggio = "\"1234\"L"
	#send(messaggio)
	messaggio = "700H2T 1000H10T  15000H1T"
	#send(messaggio)
	
	messaggio = "K"
	#send(messaggio)

	messaggio = "3500H7R  8056H2R 6654H4R"
	#send(messaggio)
	messaggio = "\"1234\"L"
	#send(messaggio)
	messaggio = "7T"
	#send(messaggio)
	
	messaggio = "K"
	#send(messaggio)
	
	messaggio = "2817H8R 3889H1R 6700H3R 1300H4R"
	#send(messaggio)
	messaggio = "\"1234\"L"
	#send(messaggio)
	messaggio = "1000H89T 15000H1T"
	#send(messaggio)
	
	messaggio = "K"
	#send(messaggio)
	
	messaggio = "2889H6R 8888H9R 2200H23R"
	#send(messaggio)
	messaggio = "\"1234\"L"
	#send(messaggio)
	messaggio = "10000H8T 1T"
	#send(messaggio)

	messaggio = "K"
	#send(messaggio)
	
	messaggio = "3800H1R 1333H3R 2000H23R"
	#send(messaggio)
	messaggio = "\"1234\"L"
	#send(messaggio)
	messaggio = "1000H5T 5200H1T"
	#send(messaggio)
	
	messaggio = "K"
	#send(messaggio)
	
	messaggio = "2346H1R 2000H23R"
	#send(messaggio)
	messaggio = "\"1234\"L"
	#send(messaggio)
	messaggio = "1500H10T 2400H1T"
	#send(messaggio)
	
	messaggio = "K"
	#send(messaggio)
	
	messaggio = "3345H1R 2000H21R"
	#send(messaggio)
	messaggio = "\"1234\"L"
	#send(messaggio)
	messaggio = "1000H12T 3000H1T"
	#send(messaggio)
	
	messaggio = "K"
	#send(messaggio)
	
	messaggio = "3346H1R 2000H1R"
	#send(messaggio)
	messaggio = "\"1234\"L"
	#send(messaggio)
	messaggio = "2000H19T  1T"
	#send(messaggio)
	

	#send(messaggio)
	#messaggio = "1F"
	#send(messaggio)
	#messaggio = "K"
	#send(messaggio)

	print count
	time.sleep(2)

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

	messaggio = "2000H1V"
	send(messaggio)
	messaggio = "K"
	send(messaggio,opened_socket)
	time.sleep(2)
	messaggio = "2000H2V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	time.sleep(2)
	messaggio = "2000H3V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	time.sleep(2)
	messaggio = "2000H4V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	time.sleep(2)
	messaggio = "2000H5V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	time.sleep(2)
	messaggio = "2000H6V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	time.sleep(2)
	messaggio = "2000H7V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	time.sleep(2)
	messaggio = "2000H8V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	time.sleep(2)
	messaggio = "2000H9V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	messaggio = "2000H10V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	messaggio = "2000H11V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "2000H12V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	messaggio = "2000H13V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
	messaggio = "2000H14V"
	send(messaggio,opened_socket)
	messaggio = "K"
	send(messaggio,opened_socket)
'''