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
	
ip = "192.168.1.169"
#ip = "192.168.1.237"
port =9101

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
	s = '023F2F313003'
	s= '\/80////1234567890/////////sseapid.isti.cnr.it/sseapid.isti.cnr.it//////'
	invia  =  s#.decode('hex')
	send2(invia)
	s = '3/S/%22 BENE//1/1/1///0/0/'
	invia  =  s#.decode('hex')
	send2(invia)
	s= '5/1/0'
	invia  =  s#.decode('hex')
	send2(invia)
	time.sleep(2)
	s = 'x/7'
	invia  =  s#.decode('hex')
	send2(invia)
	
	
exit(0)
for cicli in range(2,102):
	send2("-/"+date+"/"+str(z)+"/"+str(i)+"//")
	#send2('I/123456789/0/')
	send2('3/N/test_01//1/20.0/1//')
	#send2('3/S/test_01//1/20.0/1//')
	#send2('I/12345678/0/')
	send2('5/4/0.00////')
	i+=1
	print cicli
	time.sleep(5)


exit(0)
'''
'''

date = "160921"
z = 38
ndoc = 1
#annullo
for cicli in range(1,9):
	send2("+/1/"+date+"/"+str(z)+"/"+str(ndoc)+"/")
	ndoc = ndoc + 1
	time.sleep(2)

exit(0)
#-/GGMMAA/////POS/
#+/1/GGMMAA/////POS/
date = "06092021"
send2("+/1/"+date+"/////ND/")
send2('3/B/%22 BENE//1/50.00/4/22.00//0/0/')
#send2('I/12345678/0/')
#send2('3/B/%22 BENE//1/50.00/4/22.00//0/0/')
#send2('3/N/%4 BENE//1/24.05/1/4.00//0/0/')
#send2('3/N/%10 SERVIZIO//1/122.01/13/10.00//0/1/')
#send2('3/N/%10 SERVIZIO//1/20.00/13/10.00//0/1/')
time.sleep(2)
#send2('5/14/22.00////')
#send2('5/3/7.00////')
#send2('5/6/7.00////')
#send2('5/4/50.00////')
send2('5/1/190.00////')

exit(0)
z = 5
ndoc = 3
date = "06092021"
Matricola = "8AMTN555555"
#reso
send2("-/"+date+"/"+str(z)+"/"+str(ndoc)+"/8AMTN555555/")
send2('3/N/%22 BENE//1/150.00/4/22.00//0/0/')
send2('I/12345678/0/')
send2('3/B/%22 BENE//1/50.00/4/22.00//0/0/')
send2('3/N/%4 BENE//1/24.05/1/4.00//0/0/')
send2('3/N/%10 SERVIZIO//1/122.01/13/10.00//0/1/')
send2('3/N/%10 SERVIZIO//1/20.00/13/10.00//0/1/')
time.sleep(2)
send2('5/14/22.00////')
send2('5/3/7.00////')
send2('5/6/7.00////')
send2('5/4/120.00////')
send2('5/1/110.06////')
