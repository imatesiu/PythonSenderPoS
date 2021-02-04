#!/usr/bin/python
import socket 
import time

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
	
	
ip = "192.168.1.56"
#cash port =1126
port =9150 #go
opened_socket = conn(ip,port)
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
k = 16
onetoten = range(1,2)
for count in onetoten:
	print count
	#messaggio = "K"
	#send(messaggio)
	
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	send(messaggio)
	messaggio = "15000H3R 5000H3V 12201H2R 2404H1R 2000H7R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "2200H6T 1T"
	send(messaggio)
	#messaggio = "12000H1T"
	time.sleep(2)
	#exit(0)
	
	#messaggio = "K"
	#send(messaggio)	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	
	send(messaggio)
	messaggio = "13322H2R 3300H2V 3300H21R 3789H1R 2456H10R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "700H2T 1000H10T  15000H1T"
	send(messaggio)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	
	send(messaggio)
	messaggio = "3500H7R  8056H2R 6654H4R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "7T"
	send(messaggio)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	
	send(messaggio)
	messaggio = "2817H8R 3889H1R 6700H3R 1300H4R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "1000H89T 15000H1T"
	send(messaggio)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	
	send(messaggio)
	messaggio = "2889H6R 8888H9R 2200H23R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "10000H8T 1T"
	send(messaggio)

	time.sleep(2)
	messaggio = "K"
	send(messaggio)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	
	send(messaggio)
	messaggio = "3800H1R 1333H3R 2000H23R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "5200H1T"
	send(messaggio)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	
	send(messaggio)
	messaggio = "2346H1R 2000H23R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "1500H10T 2400H1T"
	send(messaggio)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"

	send(messaggio)
	messaggio = "3345H1R 2000H21R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "1000H12T 3000H1T"
	send(messaggio)
	
	time.sleep(2)
	messaggio = "K"
	send(messaggio)
	
	messaggio = "K"
	doc +=1
	messaggio = "\""+str(k).zfill(4)+"-"+str(doc).zfill(4)+"-10082020-4CIDN000001\"104M"
	send(messaggio)
	messaggio = "3346H1R 2000H1R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "2000H19T  1T"
	send(messaggio)
	

	#send(messaggio)
	#messaggio = "1F"
	#send(messaggio)
	#messaggio = "K"
	#send(messaggio)

	print count
	time.sleep(1)

exit(0) 
'''

doc = 1
onetoten = range(1,11)
for count in onetoten:

	
	
	messaggio = "\"0025-"+str(doc).zfill(4)+"-31102020\"105M"
	send(messaggio)
	doc +=1

	#send(messaggio)
	#messaggio = "1F"
	#send(messaggio)
	#messaggio = "K"
	#send(messaggio)

	print count
	time.sleep(1)

exit(0)

onetoten = range(1,2)
for count in onetoten:
	messaggio = "K"
	send(messaggio)
	messaggio = "15000H3R 5000H3V 12201H2R 2404H1R 2000H7R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "2200H6T 700H2T  12000H3T 11705H1T"
	send(messaggio)
	time.sleep(4)
	messaggio = "13322H2R 3300H2V 3300H21R 3789H1R 2456H10R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "700H2T 1000H10T  15000H1T"
	send(messaggio)
	time.sleep(4)
	messaggio = "K"
	send(messaggio)
	messaggio = "3500H7R  8056H2R 6654H4R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "7T"
	send(messaggio)
	time.sleep(4)
	messaggio = "K"
	send(messaggio)
	messaggio = "2817H8R 3889H1R 6700H3R 1300H4R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "1000H89T 15000H1T"
	send(messaggio)
	time.sleep(4)
	messaggio = "K"
	send(messaggio)
	messaggio = "2889H6R 8888H9R 2200H23R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "10000H8T 1T"
	send(messaggio)
	time.sleep(4)
	messaggio = "K"
	send(messaggio)
	messaggio = "3800H1R 1333H3R 2000H23R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "5200H1T"
	send(messaggio)
	time.sleep(4)
	messaggio = "K"
	send(messaggio)
	messaggio = "2346H1R 2000H23R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "1500H10T 2400H1T"
	send(messaggio)
	time.sleep(4)
	messaggio = "K"
	send(messaggio)
	messaggio = "3345H1R 2000H21R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "1000H12T 3000H1T"
	send(messaggio)
	time.sleep(4)
	messaggio = "K"
	send(messaggio)
	messaggio = "3346H1R 2000H1R"
	send(messaggio)
	messaggio = "\"1234\"L"
	send(messaggio)
	messaggio = "2000H19T 345H11T 1T"
	send(messaggio)
	#messaggio = "K"
	#send(messaggio)
	''' 
	messaggio = "15000H3R 5000H3V 12201H2R 2404H1R 2000H7R"
	print(messaggio)
	#time.sleep(10)
	messaggio = "\"1234\"L"
	print(messaggio)
	#time.sleep(10)
	messaggio = "2200H6T 700H2T  12000H3T 11705H1T"
	print(messaggio)
	#time.sleep(10)
	messaggio = "13322H2R 3300H2V 3300H21R 3789H1R 2456H10R"
	print(messaggio)
	messaggio = "\"1234\"L"
	print(messaggio)
	messaggio = "700H2T 1000H10T  15000H1T"
	print(messaggio)
	
	messaggio = "K"
	print(messaggio)

	messaggio = "3500H7R  8056H2R 6654H4R"
	print(messaggio)
	messaggio = "\"1234\"L"
	print(messaggio)
	messaggio = "7T"
	print(messaggio)
	
	messaggio = "K"
	print(messaggio)
	
	messaggio = "2817H8R 3889H1R 6700H3R 1300H4R"
	print(messaggio)
	messaggio = "\"1234\"L"
	print(messaggio)
	messaggio = "1000H89T 15000H1T"
	print(messaggio)
	
	messaggio = "K"
	print(messaggio)
	
	messaggio = "2889H6R 8888H9R 2200H23R"
	print(messaggio)
	messaggio = "\"1234\"L"
	print(messaggio)
	messaggio = "10000H8T 1T"
	print(messaggio)

	messaggio = "K"
	print(messaggio)
	
	messaggio = "3800H1R 1333H3R 2000H23R"
	print(messaggio)
	messaggio = "\"1234\"L"
	print(messaggio)
	messaggio = "1000H5T 5200H1T"
	print(messaggio)
	
	messaggio = "K"
	print(messaggio)
	
	messaggio = "2346H1R 2000H23R"
	print(messaggio)
	messaggio = "\"1234\"L"
	print(messaggio)
	messaggio = "1500H10T 2400H1T"
	print(messaggio)
	
	messaggio = "K"
	print(messaggio)
	
	messaggio = "3345H1R 2000H21R"
	print(messaggio)
	messaggio = "\"1234\"L"
	print(messaggio)
	messaggio = "1000H12T 3000H1T"
	print(messaggio)
	
	messaggio = "K"
	print(messaggio)
	
	messaggio = "3346H1R 2000H1R"
	print(messaggio)
	messaggio = "\"1234\"L"
	print(messaggio)
	messaggio = "2000H19T  1T"
	print(messaggio)
	
'''
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
	send(messaggio)
	time.sleep(2)
	messaggio = "2000H2V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	time.sleep(2)
	messaggio = "2000H3V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	time.sleep(2)
	messaggio = "2000H4V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	time.sleep(2)
	messaggio = "2000H5V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	time.sleep(2)
	messaggio = "2000H6V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	time.sleep(2)
	messaggio = "2000H7V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	time.sleep(2)
	messaggio = "2000H8V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	time.sleep(2)
	messaggio = "2000H9V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	messaggio = "2000H10V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	messaggio = "2000H11V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	
	messaggio = "2000H12V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	messaggio = "2000H13V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
	messaggio = "2000H14V"
	send(messaggio)
	messaggio = "K"
	send(messaggio)
'''