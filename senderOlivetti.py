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
	
ip = "192.168.1.611"
port =9000

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
	s = '022431333232213203'
	invia  =  s.decode('hex')
	send2(invia)
	s = '022431333232213203'
	invia  =  s.decode('hex')
	send2(invia)
	s= '0224313332352531302c30302d56656e64697461204956412031213103'
	invia  =  s.decode('hex')
	send2(invia)
	time.sleep(2)
	s = '02243133353521312531302c303003'
	invia  =  s.decode('hex')
	send2(invia)
	s = '0224313332352531302c30302d56656e64697461204956412032213203'
	invia  =  s.decode('hex')
	send2(invia)

	s = '02243133323903'
	invia  =  s.decode('hex')
	send2(invia)

	s = '02243133323303'
	invia  =  s.decode('hex')
	send2(invia)
	
	
	#chiusura
	s = '022333313221312a5265706f72742031303a03'
	invia  =  s.decode('hex')
	send2(invia)
	s = '022333313221322d5a3130202d2066697363616c6503'
	invia  =  s.decode('hex')
	send2(invia)
	
	s = '02243133333303'
	invia  =  s.decode('hex')
	send2(invia)
	s = '0223333132213136526573657420636f6e7461746f72692028313333342903'
	invia  =  s.decode('hex')
	send2(invia)
	s = '02233331322132212003'
	invia  =  s.decode('hex')
	send2(invia)
	s = '02243133333403'
	invia  =  s.decode('hex')
	send2(invia)
	s = '022333313221323633302f30362f323032322c2031363a32373a31362e3503'
	invia  =  s.decode('hex')
	send2(invia)
	i+=1
	print cicli
	time.sleep(10)
	
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
