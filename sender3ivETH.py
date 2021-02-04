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
	#print res
	
	
ip = "192.168.1.10"
#cash port =1126
port =1723

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


k=60
opened_socket = conn(ip,port)
send("\"12345678\"38F")
exit(0)
'''send("\"12345678\"38F")
send("15000H3R")
send("=")
send("102T")

exit(0)'''
'''
send("\"12345678\"38F")
send("15000H23R")
send("5000H14M")
send("2405H21R")
send("12201H2R")
send("2000H7R")
send("=")
send("700H105T")
send("700H2T")
send("12000H3T")
send("2200H103T")
send("1T")
time.sleep(13)
send("13322H22R")
send("\"12345678\"38F")
send("2000H14M")
send("3300H21R")
send("3300H13M")
send("3789H3R")
send("2456H16R")
send("=")
send("200H105T")
send("2000H103T")
send("1000H106T")
send("15000H1T")
time.sleep(10)
send("\"12345678\"38F")
send("3500H27R")
send("2000H14M")
send("5600H21R")
send("6654H4R")
send("1256H1R")
send("=")
send("104T")
time.sleep(13)
send("\"12345678\"38F")
send("2817H28R")
send("1000H16M")
send("3889H21R")
send("6700H3R")
send("1300H1R")
send("=")
send("1000H107T")
send("1500H106T")
send("700H105T")
send("12000H1T")
time.sleep(13)
send("\"12345678\"38F")
send("2889H26R")
send("8888H29R")
send("2000H23R")
send("2000H13M")
send("=")
send("102T")
time.sleep(10)
send("\"12345678\"38F")
send("3800H21R")
send("1333H23R")
send("2000H3R")
send("2000H13M")
send("=")
send("1T")
time.sleep(13)
send("\"12345678\"38F")
send("2647H21R")
send("2000H23R")
send("2000H13M")
send("=")
send("1T")
time.sleep(10)
send("\"12345678\"38F")
send("3345H21R")
send("2000H21R")
send("2000H13M")
send("=")
send("345H100T")
send("3000H1T")
'''
'''
send("\""+str(k).zfill(4)+"-0001\"51F")

send("15000H23R")
send("5000H14M")
send("2405H21R")
send("12201H2R")
send("2000H7R")
send("=")
send("700H105T")
send("700H2T")
send("12000H3T")
send("2200H103T")
send("1T")
time.sleep(13)
send("\""+str(k).zfill(4)+"-0002\"51F")
send("13322H22R")
send("2000H14M")
send("3300H21R")
send("3300H13M")
send("3789H3R")
send("2456H16R")
send("=")
send("200H105T")
send("2000H103T")
send("1000H106T")
send("15000H1T")
time.sleep(13)
send("\""+str(k).zfill(4)+"-0003\"51F")
send("3500H27R")
send("2000H14M")
send("5600H21R")
send("6654H4R")
send("1256H1R")
send("=")
send("104T")
time.sleep(13)
send("\""+str(k).zfill(4)+"-0004\"51F")
send("2817H28R")
send("1000H16M")
send("3889H21R")
send("6700H3R")
send("1300H1R")
send("=")
send("1000H107T")
send("1500H106T")
send("700H105T")
send("12000H1T")
time.sleep(13)
send("\""+str(k).zfill(4)+"-0005\"51F")
send("2889H26R")
send("8888H29R")
send("2000H23R")
send("2000H13M")
send("=")
send("102T")
time.sleep(13)
send("\""+str(k).zfill(4)+"-0006\"51F")
send("3800H21R")
send("1333H23R")
send("2000H3R")
send("2000H13M")
send("=")
send("1T")
time.sleep(13)
send("\""+str(k).zfill(4)+"-0007\"51F")
send("2647H21R")
send("2000H23R")
send("2000H13M")
send("=")
send("1T")
time.sleep(13)
send("\""+str(k).zfill(4)+"-0008\"51F")
send("3345H21R")
send("2000H21R")
send("2000H13M")
send("=")'''
send("3000H1T")
send("345H100T")


exit(0)

send("z1Fc")
exit(0)



k=58
for count in range(1,10):
	messaggio = "\""+str(k).zfill(4)+"-"+str(count).zfill(4)+"\"52F"
	send(messaggio)
	time.sleep(20)
send("z1Fc")
exit(0)	

#"0100-0002"52F
#send("5M500031R 5*1000H1R 10000H7R = 10000H1T 8000H3T 2000H2T")
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
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "2200H6T 700H2T  12000H3T 12000H1T"
	send(messaggio,opened_socket)
	#messaggio = "12000H1T"
	#messaggio = "K"
	#send(messaggio,opened_socket)
	exit(0)
	messaggio = "13322H2R 3300H2V 3300H21R 3789H1R 2456H10R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "700H2T 1000H10T  15000H1T"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	send(messaggio,opened_socket)

	messaggio = "3500H7R  8056H2R 6654H4R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "7T"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "2817H8R 3889H1R 6700H3R 1300H4R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "1000H89T 15000H1T"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "2889H6R 8888H9R 2200H23R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "10000H8T 1T"
	send(messaggio,opened_socket)

	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "3800H1R 1333H3R 2000H23R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "1000H5T 5200H1T"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "2346H1R 2000H23R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "1500H10T 2400H1T"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "3345H1R 2000H21R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "1000H12T 3000H1T"
	send(messaggio,opened_socket)
	
	messaggio = "K"
	send(messaggio,opened_socket)
	
	messaggio = "3346H1R 2000H1R"
	send(messaggio,opened_socket)
	messaggio = "\"1234\"L"
	send(messaggio,opened_socket)
	messaggio = "2000H19T  1T"
	send(messaggio,opened_socket)
	

	send(messaggio,opened_socket)
	messaggio = "1F"
	#send(messaggio,opened_socket)
	#messaggio = "K"
	#send(messaggio,opened_socket)

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
	send(messaggio,opened_socket)
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