import requests
import time
from base64 import b64encode
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import datetime as date
import hashlib
import re
from datetime import datetime
from xml.etree import ElementTree


def createhash(content):
    sha256 = hashlib.sha256(content.encode('utf-8'))
   # sha256.update()
    return sha256.hexdigest()

#  hash_object = hashlib.sha256(result_to_secure.encode('utf-8'))
 #   hex_dig = hash_object.hexdigest()
#test = "<receipt><hash fingerPrint=\"a89002dd7ce1b087ddfeaba5656bd8856f3d7dbce09633e01d0f38faa8605287\"/><printerFiscalReceipt><printRecMessage message=\"RESO MERCE N.0040-0002 del 23-10-2017\" messageType=\"1\"/><beginFiscalReceipt/><printRecItem description=\"VAT ID 1\" quantity=\"1\" unitPrice=\"20,00\" vatID=\"1\"/><fiscalInformation cashAmount=\"0,00\" changeAmount=\"0,00\" dailyAmount=\"0\" dateTime=\"20171023T104931\" docType=\"2\" ePayAmount=\"0,00\" noPayAmount=\"0,00\" paidAmount=\"20,00\" recAmount=\"20,00\" recNumber=\"0002\" recVAT=\"3,61\" tillId=\"BBBB0001\" zRepNumber=\"0044\"/><endFiscalReceipt/></printerFiscalReceipt></receipt>"
#print createhash(test)
#exit(0)
set_ip_server = "146.48.84.159"
urlcassa = "https://"+set_ip_server+"/cgi-bin/fpserver.cgi?timeout=10000"
#set_ip_apparato = "192.168.1.136"

cassa_matricola = "AAAA0001"



def send_postBasicAuth(content):
	response = requests.post('https://'+set_ip_server+'/cgi-bin/fpserver.cgi',data=content,auth=HTTPBasicAuth(cassa_matricola, 'epson'),headers={"Content-Type": "application/soap+xml" }, verify=False)
	#response = requests.post('http://'+set_ip_apparato+':80/cgi-bin/epos/service.cgi?devid=local_printer',data=content,headers={"Content-Type": "application/soap+xml"})
	print response.text
	assert response.status_code == 200
	return response.text
	
def send_post(content):
	response = requests.post('https://'+set_ip_server+'/cgi-bin/fpserver.cgi',data=content,auth=HTTPBasicAuth(cassa_matricola, 'epson'),headers={"Content-Type": "application/soap+xml" }, verify=False)
	#response = requests.post('http://'+set_ip_apparato+':80/cgi-bin/epos/service.cgi?devid=local_printer',data=content,headers={"Content-Type": "application/soap+xml"})
	print response.text
	assert response.status_code == 200
	return response.text
    
def send_post2(content):
	response = requests.post('https://'+set_ip_server+'/cgi-bin/fpmate.cgi',data=content,auth=HTTPBasicAuth(cassa_matricola, 'epson'),headers={"Content-Type": "application/soap+xml" }, verify=False)
	#response = requests.post('http://'+set_ip_apparato+':80/cgi-bin/epos/service.cgi?devid=local_printer',data=content,headers={"Content-Type": "application/soap+xml"})
	print response.text
	assert response.status_code == 200
	return response.text       

    
def request_token(cassa):
	token = "<createToken><till tillId=\""+cassa+"\" /></createToken>"
	soaptoken = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body>"+token+"</soapenv:Body></soapenv:Envelope>"
	print soaptoken
	reply = send_post(soaptoken)
	regex = r"token>.*"
	matches = re.findall(regex, reply)
	for matche in matches:
		token = matche.replace("</token>","").replace("token>","")
		ndoc = int(token[36:40])
		znum = token[32:36]
		return token,token[:44], float(token[44:])/100, int(ndoc),znum

for i in range(1):
	token,tok,dailyamount,ndoc,znum = request_token(cassa_matricola)
	print token
	#
	print tok
	print ndoc
	print znum
	#exit(0)

	#dailyamount += 0.2
	#ndoc +=1
	daten =  datetime.now().strftime('%Y%m%dT%H%M%S') #20171023T085606
	dailyaa = float(dailyamount) + float(10.9)
	#print dailyaa
	scontrino = "<receipt><hash fingerPrint=\""+token+"\"/><printerFiscalReceipt><beginFiscalReceipt/><printRecItem description=\"VAT ID 1\" quantity=\"1\" unitPrice=\"10,00\" vatID=\"1\"/><printRecItem description=\"VAT ID 2\" quantity=\"1\" unitPrice=\"0,20\" vatID=\"2\"/><printRecItem description=\"VAT ID 3\" quantity=\"1\" unitPrice=\"0,30\" vatID=\"3\"/><printRecItem description=\"VAT ID 0\" quantity=\"1\" unitPrice=\"0,40\" vatID=\"0\"/><printRecTotal description=\"PAGAMENTO CONTANTE\" index=\"0\" payment=\"0\" paymentType=\"0\"/><fiscalInformation cashAmount=\"10,90\" changeAmount=\"0,00\" dailyAmount=\""+str(dailyaa).replace(".",",")+"\" dateTime=\""+daten+"\" docType=\"0\" ePayAmount=\"00,00\" noPayAmount=\"0,00\" paidAmount=\"10,90\" recAmount=\"10,90\" recNumber=\""+str(ndoc).zfill(4)+"\" recVAT=\"1,83\" tillId=\""+cassa_matricola+"\" zRepNumber=\""+znum+"\"/><endFiscalReceipt/></printerFiscalReceipt></receipt>"

	hash = createhash(scontrino)

	send = "<createReceipt>"+scontrino+"<receiptSecurity><hash fingerPrint=\""+hash+"\"/></receiptSecurity></createReceipt>"



	print 
	#print send

	soap = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body>"+send+"</soapenv:Body></soapenv:Envelope>"

	print soap

	#soap2 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body>"+send2+"</soapenv:Body></soapenv:Envelope>"

	#print soap2

	send_post(soap)

	#send_post(soap)
	#send_post(soap2)
	#send_post(soap)
	#send_post(soap)


	chiusaracassa = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\"><SOAP-ENV:Header/><SOAP-ENV:Body><createDailyClosure><till tillId=\"AAAA0001\" /></createDailyClosure></SOAP-ENV:Body></SOAP-ENV:Envelope>"

	send_post(chiusaracassa)

	chiusuraRT = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\"><SOAP-ENV:Header/><SOAP-ENV:Body><printerFiscalReport><printZReport operator=\"1\" /></printerFiscalReport></SOAP-ENV:Body></SOAP-ENV:Envelope>"

	chiusuraRT2 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body><printerFiscalReport><printZReport operator=\"1\" /></printerFiscalReport></soapenv:Body></soapenv:Envelope>"

	#print chiusuraRT2
	send_post2(chiusuraRT2)
	print i


exit(0)

#99SEA000217AAAA0001143902017111300270002000063570

'''
	dailyaa += float(10.9)

	scontrino2 = "<receipt><hash fingerPrint=\""+hash+"\"/><printerFiscalReceipt><beginFiscalReceipt/><printRecItem description=\"VAT ID 1\" quantity=\"1\" unitPrice=\"10,00\" vatID=\"1\"/><printRecItem description=\"VAT ID 2\" quantity=\"1\" unitPrice=\"0,20\" vatID=\"2\"/><printRecItem description=\"VAT ID 3\" quantity=\"1\" unitPrice=\"0,30\" vatID=\"3\"/><printRecItem description=\"VAT ID 0\" quantity=\"1\" unitPrice=\"0,40\" vatID=\"0\"/><printRecTotal description=\"PAGAMENTO CONTANTE\" index=\"0\" payment=\"0\" paymentType=\"0\"/><fiscalInformation cashAmount=\"10,90\" changeAmount=\"0,00\" dailyAmount=\""+str(dailyaa).replace(".",",")+"\" dateTime=\""+daten+"\" docType=\"0\" ePayAmount=\"00,00\" noPayAmount=\"0,00\" paidAmount=\"10,90\" recAmount=\"10,90\" recNumber=\""+str(ndoc).zfill(4)+"\" recVAT=\"1,83\" tillId=\""+cassa_matricola+"\" zRepNumber=\""+znum+"\"/><endFiscalReceipt/></printerFiscalReceipt></receipt>"
	hash2 = createhash(scontrino2)
	send2 = "<createReceipt>"+scontrino2+"<receiptSecurity><hash fingerPrint=\""+hash2+"\"/></receiptSecurity></createReceipt>"

'''

