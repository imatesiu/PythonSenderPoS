import requests
import time
from base64 import b64encode
from requests.auth import HTTPDigestAuth
import datetime as date
import hashlib
import re
from datetime import datetime


def createhash(content):
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()

#test = "<receipt><hash fingerPrint=\"a89002dd7ce1b087ddfeaba5656bd8856f3d7dbce09633e01d0f38faa8605287\"/><printerFiscalReceipt><printRecMessage message=\"RESO MERCE N.0040-0002 del 23-10-2017\" messageType=\"1\"/><beginFiscalReceipt/><printRecItem description=\"VAT ID 1\" quantity=\"1\" unitPrice=\"20,00\" vatID=\"1\"/><fiscalInformation cashAmount=\"0,00\" changeAmount=\"0,00\" dailyAmount=\"0\" dateTime=\"20171023T104931\" docType=\"2\" ePayAmount=\"0,00\" noPayAmount=\"0,00\" paidAmount=\"20,00\" recAmount=\"20,00\" recNumber=\"0002\" recVAT=\"3,61\" tillId=\"BBBB0001\" zRepNumber=\"0044\"/><endFiscalReceipt/></printerFiscalReceipt></receipt>"
#print createhash(test)
#exit(0)

set_ip_apparato = "10.0.0.100"
set_ip_server = "10.0.0.90"


def send_post(content):
	response = requests.post('https://'+set_ip_server+'/cgi-bin/fpserver.cgi',data=content,auth=HTTPDigestAuth('AAAA0002', 'epson'),headers={"Content-Type": "application/soap+xml" }, verify=False)
	#response = requests.post('http://'+set_ip_apparato+':80/cgi-bin/epos/service.cgi?devid=local_printer',data=content,headers={"Content-Type": "application/soap+xml"})
	print response.text
	assert response.status_code == 200
	return response.text
	
def request_token():
	token = "<createToken><till tillId=\"AAAA0002\" /></createToken>"
	soaptoken = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body>"+token+"</soapenv:Body></soapenv:Envelope>"
	reply = send_post(soaptoken)
	regex = r"token>.*"
	matches = re.findall(regex, reply)
	for matche in matches:
		token = matche.replace("</token>","").replace("token>","")
		ndoc = int(token[36:40])
		znum = token[32:36]
		return token,token[:44], float(token[44:])/100, int(ndoc),znum
	exit(0)





token,tok,dailyamount,ndoc,znum = request_token()
print token
print dailyamount
print ndoc
print znum
#exit(0)

dailyamount += 0.2
ndoc +=2
daten =  datetime.now().strftime('%Y%m%dT%H%M%S') #20171023T085606

scontrino = "<receipt><hash fingerPrint=\""+token+"\"/><printerFiscalReceipt><beginFiscalReceipt/><printRecItem description=\"VAT ID 1\" quantity=\"1\" unitPrice=\"-10,00\" vatID=\"1\"/><printRecItem description=\"VAT ID 2\" quantity=\"1\" unitPrice=\"0,20\" vatID=\"2\"/><printRecItem description=\"VAT ID 3\" quantity=\"1\" unitPrice=\"-0,30\" vatID=\"3\"/><printRecItem description=\"VAT ID 0\" quantity=\"1\" unitPrice=\"-0,40\" vatID=\"0\"/><printRecTotal description=\"PAGAMENTO CONTANTE\" index=\"0\" payment=\"0\" paymentType=\"0\"/><fiscalInformation cashAmount=\"-10,50\" changeAmount=\"0,00\" dailyAmount=\""+str(dailyamount).replace(".",",")+"\" dateTime=\""+daten+"\" docType=\"0\" ePayAmount=\"-10,00\" noPayAmount=\"0,00\" paidAmount=\"-10,50\" recAmount=\"-10,50\" recNumber=\""+str(ndoc).zfill(4)+"\" recVAT=\"-1,83\" tillId=\"AAAA0002\" zRepNumber=\""+znum+"\"/><endFiscalReceipt/></printerFiscalReceipt></receipt>"

hash = createhash(scontrino)

send = "<createReceipt>"+scontrino+"<receiptSecurity><hash fingerPrint=\""+hash+"\"/></receiptSecurity></createReceipt>"




soap = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body>"+send+"</soapenv:Body></soapenv:Envelope>"



send_post(soap)



#send_post_apparato(soap)


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