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
	data = opened_socket.recv(2048)
	print data
	time.sleep(2)
	

	
	
ip = "10.0.30.23"
port =1034

opened_socket = conn(ip,port)

def send2(msg):
  try:
	opened_socket2 = socket.socket(socket.AF_INET,  socket.SOCK_STREAM) 
	opened_socket2.connect((ip, port))
	print msg
	opened_socket2.send(msg)
	data = opened_socket2.recv(2048)
	print data
	opened_socket2.close()
	time.sleep(2)
  except Exception as e:
  	print str(e)

k=147
'''
0230313030324e3d4b31333803
0230313030334e3d433132303303
0230313032314e3d52332f243330302f2841525449434f4c4f20332933313503
0230313032314e3d52342f243430302f2841525449434f4c4f20342934313503
0230313030384e3d54312f2437303035323403
0230313030324e3d6336313703
0230313030334e3d433337303403
0230313030344e3d43313038334503
'''

#Lotteria
#
z = 29
ndoc = 1
date = "17052022"
Matricola = ""
#reso
i = 1 
for cicli in range(1,600):
	
	s = '0230313030324e3d4b31333803'
	invia  =  s.decode('hex')
	send(invia)
	
	#s = "\0201003N=C1203\03"
	s = '0230313030334e3d433132303303'
	invia  =  s.decode('hex')
	send(invia)
	
	#s = "\0201019N=R1/$150/(BENE \"A\")364\03"
	s = '0230313032314e3d52332f243330302f2841525449434f4c4f20332933313503'
	invia  =  s.decode('hex')
	send(invia)
	
	#s = "\0201003N=T1412\03"
	s = '0230313032314e3d52342f243430302f2841525449434f4c4f20342934313503'
	invia  =  s.decode('hex')
	send(invia)
	
	#s = "\0201002N=c514\03"
	s = '0230313030384e3d54312f2437303035323403'
	invia  =  s.decode('hex')
	send(invia)
	
	#d = "\x0201003N=C3407\x03"
	s = '0230313030324e3d6336313703'
	invia  =  s.decode('hex')
	send(invia)
	#d1 = "\x0201004N=C10533\x03"
	s = '0230313030334e3d433337303403'
	invia  =  s.decode('hex')
	send(invia)
	#send2(d)
	#send2(d1)
	
	#chiusura
	s = '0230313030344e3d43313038334503'
	invia  =  s.decode('hex')
	send(invia)
	
	s = '0230313030324e3d4b31333803'
	invia  =  s.decode('hex')
	#send(invia)
	
	#s = "\0201003N=C1203\03"
	s = '0230313030334e3d433132303303'
	invia  =  s.decode('hex')
	#send(invia)
	#s = '0230313030344e3d43313032333403'
	#invia  =  s.decode('hex')
	#send2(invia)
	
	#s = '0230313030354e3c3c2f3f7336324403'
	#invia  =  s.decode('hex')
	#send2(invia)
	i+=1
	print cicli
	time.sleep(25)
	
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
