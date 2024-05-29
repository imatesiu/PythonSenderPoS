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
set_ip_server = "192.168.1.75"
urlcassa = "http://"+set_ip_server+"/cgi-bin/fpmate.cgi?timeout=10000"
#set_ip_apparato = "192.168.1.136"

cassa_matricola = "AAAA0001"



def send_postBasicAuth(content):
	response = requests.post('https://'+set_ip_server+'/cgi-bin/fpserver.cgi',data=content,auth=HTTPBasicAuth(cassa_matricola, 'epson'),headers={"Content-Type": "application/soap+xml" }, verify=False)
	#response = requests.post('http://'+set_ip_apparato+':80/cgi-bin/epos/service.cgi?devid=local_printer',data=content,headers={"Content-Type": "application/soap+xml"})
	print response.text
	assert response.status_code == 200
	return response.text
	
def send_post(content):
	soap = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body>"+content+"</soapenv:Body></soapenv:Envelope>"
	response = requests.post(urlcassa,data=soap,headers={"Content-Type": "application/soap+xml" })
	#response = requests.post('http://'+set_ip_apparato+':80/cgi-bin/epos/service.cgi?devid=local_printer',data=content,headers={"Content-Type": "application/soap+xml"})
	print response.text
	assert response.status_code == 200
	return response.text

def annullo_f(z,doc,d,m):
	annullo = "<printerFiscalReceipt><printRecMessage  operator=\"1\" messageType=\"4\" message=\"VOID "+z+" "+doc+" "+d+" "+m+"\" /></printerFiscalReceipt>"
	print annullo
	send_post(annullo)

'''
root = ElementTree.parse('esempieps.xml')
for form in root.getroot():
	stringDC = ElementTree.tostring(form, encoding='utf-8')
	send_post(stringDC)


#annulli
chiusura = 59
data = "20112020"
matricola = "99IEC000006"
for elem in range(1,9):
	z = str(chiusura).zfill(4)
	d = str(elem).zfill(4)
	annullo_f(z,d,data,matricola)

#resi
chiusura = 2
data = "20112020"
matricola = "99IEC000002"

root = ElementTree.parse('resieps.xml')
ele = 1
for form in root.getroot():
	stringDC = ElementTree.tostring(form, encoding='utf-8')
	z = str(chiusura).zfill(4)
	d = str(ele).zfill(4)
	reso = "REFUND "+str(z)+" "+str(d)+" "+data+" "+matricola+"\" operator=\"1\" messageType=\"4\"/>"
	line = re.sub("REFUND.*" , reso , stringDC)
	send_post(line)
	ele += 1



#resi pos
chiusura = 0
data = "20112020"
matricola = "POS        "

root = ElementTree.parse('resieps.xml')
ele = 1
for form in root.getroot():
	stringDC = ElementTree.tostring(form, encoding='utf-8')
	z = str(chiusura).zfill(4)
	d = str(0).zfill(4)
	reso = "REFUND "+str(z)+" "+str(d)+" "+data+" "+matricola+"\" operator=\"1\" messageType=\"4\"/>"
	line = re.sub("REFUND.*" , reso , stringDC)
	line = re.sub("<directIO.*" , "" , line)
	send_post(line)
	if(ele % 2 == 0):
		matricola = "VR         "
	if(ele % 3 == 0):
		matricola = "ND         "

'''
#annulli pos
chiusura = 0
data = "20112020"
matricola = "POS        "

root = ElementTree.parse('resieps.xml')
ele = 1
for form in root.getroot():
	stringDC = ElementTree.tostring(form, encoding='utf-8')
	z = str(chiusura).zfill(4)
	d = str(0).zfill(4)
	reso = "VOID "+str(z)+" "+str(d)+" "+data+" "+matricola+"\" operator=\"1\" messageType=\"4\"/>"
	line = re.sub("REFUND.*" , reso , stringDC)
	line = re.sub("<directIO.*" , "" , line)
	send_post(line)
	ele += 1
	if(ele % 2 == 0):
		matricola = "VR         "
	if(ele % 3 == 0):
		matricola = "ND         "

#zz
zz = "<printerFiscalReport><printZReport  operator=\"1\" /></printerFiscalReport>"
send_post(zz)
#print ElementTree.tostring(xml.getroot(), encoding='utf-8')
exit(0)

#99SEA000217AAAA0001143902017111300270002000063570


import urllib2, base64

import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

request = urllib2.Request('https://'+set_ip_server+'/cgi-bin/fpserver.cgi')
base64string = base64.encodestring('%s:%s' % ('AAAA0001', 'epson')).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)

print request
response = urllib2.urlopen(request, context=ssl._create_unverified_context())

print response
exit(0)
