#!/usr/bin/python
import sys
import urllib2, base64
import ssl
import requests
import time
from base64 import b64encode
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth
import datetime as date
import hashlib
import re
from datetime import datetime
import json
import csv
import fileinput
import hmac
import hashlib
import base64
import time
from collections import OrderedDict


user = "00010001"
lottery_client_code = "12345678"
if(len(sys.argv)>2):
	 user = sys.argv[2]
password = "admin"
set_ip_server = "192.168.1.12"
matricola = "96SRT000109"
#matricola = "53SNS310003"


def hmacsha256(key,mess):
	digest = hmac.new(bytes(key).encode('utf-8'), bytes(mess).encode('utf-8'), digestmod=hashlib.sha256).digest()
	signature = base64.b64encode(digest)
	return signature

class JSONObject:
    def __init__(self, d):
             self.__dict__ = d
             
def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ }
    d.update(vars(obj))
    return d
    
def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls)   # Make instance without calling __init__
        for key, value in d.items():
            setattr(obj, key, value)
            return obj
    else:
        return d

def loopElement(spamReader):
	for line in spamReader:
		importosenzasconto = line[0]
		importoscontato = line[1]
		imponibile = line[2]
		imposta = line[3]
		aliquota = line[4]
		percentualesconto = line[5]
		valoresconto = line[6]
		tipodocumento = line[7]
		print importosenzasconto,importoscontato,imponibile,imposta,aliquota,percentualesconto,valoresconto,tipodocumento


def createhash(content):
	sha256 = hashlib.sha256()
	sha256.update(content)
	return base64.b64encode(sha256.digest())

sendzdoc = "insertDeviceZDocument.php"
senddoc = "insertFiscalDocument.php" #"insertFiscalDocumentLottery.php" #"insertFiscalDocument.php"
getdailystatus = "getDailyStatus.php"
opendaym = "getDailyOpen.php"
sendZ = "insertZDocument.php"

def send_post(content, url):
	time.sleep(1)
	#print content, url
	response = requests.post('https://'+set_ip_server+'/'+url,data=content,auth=HTTPBasicAuth(user, password),headers={"Content-Type": "application/x-www-form-urlencoded","USER-AGENT":None,"ACCEPT":None ,"Content-Length": str(len(content))  }, verify=False)	
	#print response.text
	assert response.status_code == 200
	print "****RESPONSE****"
	print response.text
	print "****RESPONSE _ END****"
	return response.text

	
def createqrcode(shaMetadata,addInfo,signaure):
	qrdata =  {  "shaMetadata":shaMetadata,"addInfo":addInfo,"signature":signaure}
	return qrdata

def read(filename):
	spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
	header = spamReader[0]
	del spamReader[0]
	return spamReader


init = {"data" : { "cashuuid" : user}}
json_init = json.dumps(init)
response = send_post(json_init,getdailystatus)

print json_init


#json_response = json.dumps(response)
data = json.loads(response)
print data
#print type(data)
cashToken =  data["cashToken"]
cashHmacKey =  data["cashHmacKey"]
numberClosure =  data["numberClosure"]
cashLastDocNumber = data['cashLastDocNumber']

#exit(0)
print "##########"
date =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
openday = {"data" : { "cashuuid" : user, "dtime" : date}}
print openday
json_openday = json.dumps(openday)
resp = send_post(json_openday,opendaym)#opendaym
print resp
'''
resp  = { 
  "numberClosure": 13,
  "idClosure": None,
  "fiscalBoxID": None,
  "cashName": None,
  "cashShop": None,
  "cashDesc": None,
  "cashToken": "tokennnn",
  "cashHmacKey": "keyyyy",
  "cashStatus": 1,
  "cashLastDocNumber": 1,
  "grandTotalDB": None,
  "responseCode": 0,
  "responseDesc": None
}
'''

#json_response = json.dumps(resp)
data = json.loads(resp)
if(data['cashToken']!=None):
	cashToken =  data['cashToken']
if(data['cashHmacKey']!=None):	
	cashHmacKey =  data['cashHmacKey']
if(data['numberClosure']!=None):
	numberClosure =  data['numberClosure']
#

z   =  int(numberClosure)+1
ndoc = int(cashLastDocNumber)+1
print z,ndoc,cashHmacKey
print "#########createdoc########"

#exit(0)
######CREATE DOCUMENT#######


	
	
def sendlocal(matricola,user,z,ndoc,cashToken):
	doc = "{\"document\":{\"cashuuid\":\""+user+"\",\"doctype\":1,\"dtime\":\"2020-09-03 14:33:00\",\"docnumber\":"+str(ndoc)+",\"docznumber\":"+str(z)+",\"amount\":995,\"fiscalcode\":\"\",\"vatcode\":\"01718750233\",\"fiscaloperator\":null,\"businessname\":null,\"type_signature_id\":\"1\",\"prevSignature\":\""+cashToken+"\",\"errSignature\":null,\"grandTotal\":0,\"referenceClosurenumber\":-1,\"referenceDocnumber\":-1,\"referenceDtime\":null,\"err_number\":null,\"err_znumber\":null},\"items\":[{\"type\":\"1\",\"description\":\"00092 Mini Choc           10%     9,95\",\"amount\":\"995\",\"quantity\":\"1000\",\"unitprice\":\"995\",\"vatvalue\":\"10\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null},{\"type\":\"97\",\"description\":\"TOTALE COMPLESSIVO    9,95\",\"amount\":\"995\",\"quantity\":\"1000\",\"unitprice\":\"\",\"vatvalue\":\"\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null},{\"type\":\"97\",\"description\":\"DI CUI IVA                        0,90\",\"amount\":\"90\",\"quantity\":\"1000\",\"unitprice\":\"\",\"vatvalue\":\"\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null},{\"type\":\"5\",\"description\":\"PAGAMENTO CONTANTE                9,95\",\"amount\":\"995\",\"quantity\":\"1000\",\"unitprice\":\"\",\"vatvalue\":\"\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"1\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null},{\"type\":\"5\",\"description\":\"PAGAMENTO ELETTRONICO             0,00\",\"amount\":\"0\",\"quantity\":\"1000\",\"unitprice\":\"\",\"vatvalue\":\"\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"2\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null},{\"type\":\"5\",\"description\":\"NON RISCOSSO                      0,00\",\"amount\":\"0\",\"quantity\":\"1000\",\"unitprice\":\"\",\"vatvalue\":\"\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"3\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null},{\"type\":\"97\",\"description\":\"RESTO                             0,00\",\"amount\":\"0\",\"quantity\":\"1000\",\"unitprice\":\"\",\"vatvalue\":\"\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null},{\"type\":\"97\",\"description\":\"IMPORTO PAGATO                    9,95\",\"amount\":\"995\",\"quantity\":\"1000\",\"unitprice\":\"\",\"vatvalue\":\"\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null},{\"type\":\"97\",\"description\":\"03/09/2020 14:33     DOC.N.00413-00001\",\"amount\":\"995\",\"quantity\":\"1000\",\"unitprice\":\"\",\"vatvalue\":\"\",\"fiscalvoid\":\"0\",\"signid\":\"1\",\"paymentid\":\"\",\"plu\":\"\",\"department\":\"\",\"vatcode\":null}],\"taxs\":[{\"gross\":995,\"tax\":90,\"vatvalue\":10,\"vatcode\":\"\"}]}"
	jsonfiscal = "{\"fiscalData\": \"\" ,\"qrData\":{\"shaMetadata\":\"adI8CVc2v/uUTsITyPNnq3mQUXPBI/+yGi6AW2Ctxc8=\",\"addInfo\":\"01718750233;38471004;413;1\",\"signature\":\"7C/deESS1d5mBgrV6JpZFSIyxWdC5uKxrmEIhebcKlA=\"}}"
	print (jsonfiscal)
	json_init =  json.loads(jsonfiscal)
	json_doc =  json.loads(doc)
	print (json_init)
	print (doc)
	r = dict((k, str(v).replace("'","\"")) for k, v in json_init.iteritems())
	#print fiscal
	#print r
	#print "++"+json.dumps(r["fiscalData"])
	#exit(0)
	r["fiscalData"] = doc
	shaMetadata =  createhash(r["fiscalData"])
	print  shaMetadata
	addInfo = matricola+";"+user+";"+str(z)+";"+str(ndoc)
	signaure =  hmacsha256(base64.b64decode(cashHmacKey),shaMetadata+addInfo)
	qrdata =  createqrcode(shaMetadata,addInfo,signaure)
	
	r['qrData'] = qrdata
	#r = dict((k, str(v)) for k, v in fiscal.iteritems())
	jsonfiscal =  json.dumps(r, sort_keys=True)
	print jsonfiscal
	#parse(jsonfiscal)
	re = send_post(jsonfiscal,senddoc)
	
	
	print "#########"
	#re = send_post(jsonfiscal,senddoc)
	print re
	print "exit"
	exit(0)
	


def parse(text):
    try:
    	r = json.loads(text)
    	print r['fiscalData'] 
        return True
    except ValueError as e:
        print('invalid json: %s' % e)
        return None # or: raise
        
sendlocal(matricola,user,z,ndoc,cashToken)
   
