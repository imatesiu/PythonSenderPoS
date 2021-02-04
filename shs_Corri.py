#!/usr/bin/python
import socket 
import time

def send(msg,ip,port):
	print msg
	opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	opened_socket.sendto(msg, (ip, port))
	
	
	
ip = "192.168.1.48"
port = 3001

#messaggio = "\"ciao\"@"
#messaggio = "J"
messaggio = "15000H3R"
send(messaggio,ip,port)
messaggio = "2405H1R"
send(messaggio,ip,port)
messaggio = "12201H7R"
send(messaggio,ip,port)
messaggio = "200H6R"
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
send(messaggio,ip,port)
messaggio = "700H6T"
send(messaggio,ip,port)
messaggio = "700H3T"
send(messaggio,ip,port)
messaggio = "12000H2T"
send(messaggio,ip,port)
messaggio = "2000H7T"
send(messaggio,ip,port)
messaggio = "25000H1T"
send(messaggio,ip,port)

time.sleep(5)

messaggio = "13322H2R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "3789H4R7T"
send(messaggio,ip,port)
messaggio = "2456H9R"
send(messaggio,ip,port)
messaggio = "200H6T"
send(messaggio,ip,port)
messaggio = "2000H7T"
send(messaggio,ip,port)
messaggio = "1000H11T"
send(messaggio,ip,port)
messaggio = "12000H1T"
send(messaggio,ip,port)
messaggio = "20000H1T"
send(messaggio,ip,port)

time.sleep(5)

messaggio = "3500H5R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "5600H1R"
send(messaggio,ip,port)
messaggio = "6654H10R7T"
send(messaggio,ip,port)
messaggio = "1256H8R7T"
send(messaggio,ip,port)
messaggio = "2817H11R"
send(messaggio,ip,port)
messaggio = "3889H1R"
send(messaggio,ip,port)
messaggio = "6700H4R7T"
send(messaggio,ip,port)
messaggio = "1300H8R7T"
send(messaggio,ip,port)
messaggio = "8T"
send(messaggio,ip,port)

time.sleep(5)

messaggio = "2817H11R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "3889H1R"
send(messaggio,ip,port)
messaggio = "6700H4R7T"
send(messaggio,ip,port)
messaggio = "1300H8R7T"
send(messaggio,ip,port)
messaggio = "1000H12T"
send(messaggio,ip,port)
messaggio = "1500H11T"
send(messaggio,ip,port)
messaggio = "700H6T"
send(messaggio,ip,port)
messaggio = "12000H1T"
send(messaggio,ip,port)

time.sleep(5)

messaggio = "2889H12R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "8888H13R"
send(messaggio,ip,port)
messaggio = "9T"
send(messaggio,ip,port)

time.sleep(5)

messaggio = "3800H1R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "1333H3R"
send(messaggio,ip,port)
messaggio = "1T"
send(messaggio,ip,port)

time.sleep(5)

messaggio = "2647H1R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "1T"
send(messaggio,ip,port)

time.sleep(5)

messaggio = "3345H1R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "345H10T"
send(messaggio,ip,port)
messaggio = "3000H1T"
send(messaggio,ip,port)

time.sleep(5)

messaggio = "16065H3R"
send(messaggio,ip,port)
messaggio = "1065H3M"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "5000H1R"
send(messaggio,ip,port)
messaggio = "10000H5R"
send(messaggio,ip,port)
messaggio = "20000H1T"
send(messaggio,ip,port)
messaggio = "8000H2T"
send(messaggio,ip,port)
messaggio = "1000H3T"
send(messaggio,ip,port)
messaggio = "4T"
send(messaggio,ip,port)




#Modificatore per ACCONTO : 13M Esempio ACCONTO 5,00 Euro REPARTO 1 -> 
messaggio = "500H13M1R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "1T"
send(messaggio,ip,port)

#Modificatore per OMAGGIO : 14M Esempio OMAGGIO 20,00 Euro REPARTO 3 ->
messaggio = "2000H14M3R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "1T"
send(messaggio,ip,port)

#Funzione per DI CUI ACCONTO : 54F Esempio 10,00 Euro DI CUI ACCONTO -> 
messaggio = "15000H1R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "1000H54F"
send(messaggio,ip,port)
messaggio = "1T"
send(messaggio,ip,port)
 
#Funzione per BUONO MONOUSO : 55F Esempio 10,00 Euro BUONO MONOUSO -> 
messaggio = "1000H1R"
send(messaggio,ip,port)
messaggio = "\"12345678\"53F"
send(messaggio,ip,port)
messaggio = "1000H55F"
send(messaggio,ip,port)
messaggio = "1T"
send(messaggio,ip,port)

exit(0)

onetoten = range(1,2)
for count in onetoten:
	messaggio = "9000H1R"
	send(messaggio,ip,port)

	messaggio = "\"12345678\"53F"
	send(messaggio,ip,port)
	#messaggio = "2000H1T"
	#send(messaggio,ip,port)
	messaggio = "2000H2T"
	send(messaggio,ip,port)
	print "2"
	messaggio = "2000H3T"
	send(messaggio,ip,port)
	print "3"
	messaggio = "2000H4T"
	send(messaggio,ip,port)
	print "4"
	messaggio = "2000H5T"
	send(messaggio,ip,port)
	print "5"
	messaggio = "2000H6T"
	send(messaggio,ip,port)
	print "6"
	messaggio = "2000H1T"
	send(messaggio,ip,port)
	print "1"
	time.sleep(2)


exit(0)