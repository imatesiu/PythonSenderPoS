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
import binascii
import time
reload(sys)  
sys.setdefaultencoding('Cp1252')


user = "AAAA0001"
if(len(sys.argv)>2):
	 user = sys.argv[2]
password = "a"
set_ip_server = "spagnolo2.isti.cnr.it"
#matricola = "96SRT000132"
#matricola = "53SNS310003".encode('utf-8')base64.b64decode(


matricola = "88S25000036"

def hmacsha256(key,mess):
	k = base64.b64decode(key)
	digest = hmac.new(bytes(k).encode('utf-8'), bytes(mess).encode('utf-8'), digestmod=hashlib.sha256).digest()
	signature = base64.b64encode(digest)
	return signature
	
def hmactoccdc(signature):
	ccdc  = binascii.hexlify(base64.b64decode(bytes(signature).encode('utf-8')))
	return ccdc.upper()

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
	sha256.update(bytes(content).encode('utf-8'))
	return base64.b64encode(sha256.digest())

sendzdoc = "NcrServerRT/ver1/api/insertDeviceZDocument.php"
senddoc = "NcrServerRT/ver1/api/insertFiscalDocument.php"
getdailystatus = "NcrServerRT/ver1/api/getDailyStatus.php"
opendaym = "NcrServerRT/ver1/api/getDailyOpen.php"
sendZ = "NcrServerRT/ver1/api/insertZDocument.php"

def send_post(content, url):
	time.sleep(1)
	#print content, url
	response = requests.post('https://'+set_ip_server+'/'+url,data=content,auth=HTTPBasicAuth(user, password),headers={"Content-Type": "application/json","USER-AGENT":None,"ACCEPT":None ,"Content-Length": str(len(content))  }, verify=False)	
	#print response.text
	assert response.status_code == 200
	print "****RESPONSE****"
	print response.text
	print "****RESPONSE _ END****"
	return response.text

	

def read(filename):
	spamReader = list(csv.reader(open(filename,'U'), delimiter=';'))
	header = spamReader[0]
	del spamReader[0]
	return spamReader




init = {"data" : { "cashuuid" : user}}
json_init = json.dumps(init)
print json_init
response = send_post(json_init,getdailystatus)

#print json_init

'''
response  = { 
  "numberClosure": 13,
  "idClosure": None,
  "fiscalBoxID": None,
  "cashName": None,
  "cashShop": None,
  "cashDesc": None,
  "cashToken": "tokennnn",
  "cashHmacKey": "keyyyy",
  "cashStatus": 1,
  "cashLastDocNumber": None,
  "grandTotalDB": None,
  "responseCode": 0,
  "responseDesc": None
}'''

#json_response = json.dumps(response)
data = json.loads(response)
print data
#print type(data)
'''cashToken =  data["cashToken"]
cashHmacKey =  data["cashHmacKey"]
numberClosure =  data["numberClosure"]
cashLastDocNumber = data['cashLastDocNumber']'''

#exit(0)
print "##########"
date =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
openday = {"data" : { "cashuuid" : user, "dtime" : date}}
print openday
json_openday = json.dumps(openday)
resp = send_post(json_openday,opendaym)#opendaym
#print resp
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
cashToken =  data["cashToken"]
cashHmacKey =  data["cashHmacKey"]
numberClosure =  data["numberClosure"]
cashLastDocNumber = data['cashLastDocNumber']
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

def createelement(importosenzasconto,importoscontato,imponibile,imposta,aliquota,percentualesconto,valoresconto,tipodocumento):
	type = "1"
	description = "VENDITA"
	amount = 0
	vatvalue = 0
	if(tipodocumento=="TOTALE"):
		type = "97"
		description = "TOTALE  COMPLESSIVO"
		aliquota = ""
	else:
		if "N" not in aliquota:
			vatvalue = int(float(aliquota.replace(",","."))*100)
	print float(str(importoscontato).replace(",","."))	
	amount = int(float(str(importoscontato).replace(",","."))*100)
	print importoscontato
	print amount	
	element = {
	            "type":type,
	            "description":""+description+"                     "+importoscontato+" D",
	            "netamount": amount,
				"grossamount": amount,
	            "quantity":"1000",
	            "unitprice":str(importoscontato),
	            "vatvalue":vatvalue,
	            "fiscalvoid":"0",
	            "signid":"1",
	            "paymentid":"",
	            "plu":"1",
	            "department":"1",
				"exemptioncode":"",
				"vatpercentage":str(vatvalue)
	            #"vatcode":str(aliquota)
	         }
	return element

def createiva(imposta):
	iva =      {  
	            "type":"97",
	            "description":"DI CUI IVA                "+imposta+"",
	            "netamount":imposta,
				"grossamount":"0",
	            "quantity":"",
	            "unitprice":"",
	            "vatvalue":"",
	            "fiscalvoid":"0",
	            "signid":"1",
	            "paymentid":"",
	            "plu":"",
	            "department":"",
				"exemptioncode":"",
	            "vatpercentage":""
	         }
	return iva
	
def createPagContanti(importo):
	pagamento   =   {  
	            "type":"5",
	            "description":"PAGAMENTO CONTANTI "+importo,
	            "netamount":int(float(importo.replace(",","."))*100),
				"grossamount": "0",# int(float(importo.replace(",","."))*100),
	            "quantity":"1000",
	            "unitprice":"0",
	            "vatvalue":"",
	            "fiscalvoid":"",
	            "signid":"",
	            "paymentid":"1",
	            "plu":"",
	            "department":"",
	            "exemptioncode":"",
	            "vatpercentage":"0"
	         }
	return pagamento

def createPagElettronico(importo):
	pagamento   =   {  
	            "type":"5",
	            "description":"PAGAMENTO BANCOMAT "+importo,
	           "netamount":int(float(importo.replace(",","."))*100),
				"grossamount": "0",#int(float(importo.replace(",","."))*100),
	            "quantity":"1000",
	            "unitprice":"0",
	            "vatvalue":"",
	            "fiscalvoid":"",
	            "signid":"",
	            "paymentid":"2",
	            "plu":"",
	            "department":"",
	            "exemptioncode":"",
	            "vatpercentage":"0"
	         }
	return pagamento
	
	
def createqrcode(shaMetadata,addInfo,signaure):
	qrdata =  {  "shaMetadata":shaMetadata,"addInfo":addInfo,"signature":signaure}
	return qrdata
   
def createPagCredito(importo):
	pagamento   =   {  
	            "type":"5",
	            "description":"PAGAMENTO CREDITO "+importo,
	            "netamount":int(float(importo.replace(",","."))*100),
				"grossamount": "0",#int(float(importo.replace(",","."))*100),
	            "quantity":"1000",
	            "unitprice":"0",
	            "fiscalvoid":"",
	            "signid":"",
	            "paymentid":"3",
	            "plu":"",
	            "department":"",
	            "exemptioncode":"",
	            "vatpercentage":"0"
	         }
	return pagamento
	
def createresto(importo):
	pagamento   =   {  
	            "type":"97",
	            "description":"PAGAMENTO RESTO "+importo,
	            "netamount":"0",#int(float(importo.replace(",","."))*100),
				"grossamount": "0",#int(float(importo.replace(",","."))*100),
	            "quantity":"1000",
	            "unitprice":"0",
	            "fiscalvoid":"",
	            "signid":"",
	            "paymentid":"0",
	            "plu":"",
	            "department":"",
	            "exemptioncode":"",
	            "vatpercentage":"0"
	         }
	return pagamento
	
def createTAX(imponibile,imposta,aliquota,imponibile2,imposta2,aliquota2):
	taxs =  [  
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":0,
            "exemptioncode":"N1"
         },
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":0,
            "exemptioncode":"N2"
         },
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":0,
            "exemptioncode":"N3"
         },
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":0,
            "exemptioncode":"N4"
         },
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":0,
            "exemptioncode":"N5"
         },
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":0,
            "exemptioncode":"N6"
         },
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":400,
            "exemptioncode":""
         },
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":1000,
            "exemptioncode":""
         },
         {  
            "gross":0,
            "tax":0,
            "vatpercentage":2200,
            "exemptioncode":""
         }
      ]
	for tax in taxs:
		if(tax['exemptioncode'] == aliquota):
			tax['gross'] = int(float(imponibile.replace(",","."))*100)
		if(tax['exemptioncode'] == aliquota2):
			tax['gross'] = int(float(imponibile2.replace(",","."))*100)
		'''else:'''
		if ("N" not in aliquota):
			if(tax['vatpercentage'] == int(aliquota)*100):
				tax['tax'] = int(float(imposta.replace(",","."))*100)
				tax["gross"] = int(float(imponibile.replace(",","."))*100)
			
		'''if(tax['vatcode'] == aliquota2):
			tax['tax'] = imposta2
		else:'''
		if ("N" not in aliquota2):
			if(tax['vatpercentage'] == int(aliquota2)*100):
				tax['tax'] = int(float(imposta2.replace(",","."))*100)
				tax["gross"] = int(float(imponibile2.replace(",","."))*100)
	res = []
	for tax in taxs:
		if (tax["gross"] !=0):
			res.append(tax)
	return res
	#res = []
	#for tax in taxs:
	#	r = dict((k, str(v)) for k, v in tax.iteritems())
	#	res.append(r)
	#return res
      #imposta,aliquota,imposta2,aliquota2
	
def createfiscaldata(amount,importosenzasconto,element,element2,totale,iva,pagamentoC,pagamentoE,pagamentoCC,taxs,referenceClosurenumber,referenceDocnumber,doctype,z):
	fiscal = {  
  	 "fiscalData":{  
      "document":{  
         "cashuuid":user,
         "doctype":str(doctype),
         "dtime":str(date),
         "docnumber":str(ndoc),
         "docznumber":str(z),
         "trxtotal":importosenzasconto,
         "fiscalcode":matricola,
         "vatcode": matricola,
         "fiscaloperator":"Operatore 1",
         "businessname":"",
         "type_signature_id":"1",
         "prevSignature":str(cashToken),
         "errSignature":"",
         "grandTotal":amount,
         "referenceClosurenumber":str(referenceClosurenumber),
         "referenceDocnumber":str(referenceDocnumber),
         "referenceDtime":""
      },
      "items":[  
          
            element,element2
         ,totale,iva,pagamentoC,pagamentoE,pagamentoCC,createresto("0"),
         {  
            "type":"97",
            "description":""+date+"         DOC.N."+str(z).zfill(5)+"-"+str(ndoc).zfill(5)+"",
            "netamount":importosenzasconto,
			"grossamount":importosenzasconto,
            "quantity":"",
            "unitprice":"",
            "vatvalue":"",
            "fiscalvoid":"0",
            "signid":"1",
            "paymentid":"",
            "plu":"",
            "department":"",
            "vatpercentage":"",
			"exemptioncode":""
         }
      ],
      "taxes":  
         taxs
      
 	  }
	}
	return fiscal
	

def parse(text):
    try:
    	r = json.loads(text)
    	print r['fiscalData'] 
        return True
    except ValueError as e:
        print('invalid json: %s' % e)
        return None # or: raise
        
        
spamReader = read(sys.argv[1])
nline = 0
prev = {}
prev2 = {}
taxs = []
amount = 0
print "#####"
for line in spamReader:
	importosenzasconto = line[0]
	importoscontato = line[1]
	imponibile = line[2]
	imposta = line[3]
	aliquota = line[4]
	percentualesconto = line[5]
	valoresconto = line[6]
	tipodocumento = line[7]
	importosenzasconto2 = line[9]
	importoscontato2 = line[10]
	imponibile2 = line[11]
	imposta2 = line[12]
	aliquota2 = line[13]
	percentualesconto2 = line[14]
	valoresconto2 = line[15]
	tipodocumento2 = line[16]
	rif = line[8]
	referenceClosurenumber = -1
	referenceDocnumber = -1
	doctype = 1
	if(rif != "0"):
		rifsplit = rif.split(";")
		print rif
		typ = rifsplit[0]
		rifDoc = rifsplit[1]
		referenceClosurenumber = z
		referenceDocnumber = rifDoc
		if(typ == "5"):
			doctype = 5
		if(typ == "3"):
			doctype = 3
	nline +=1
	current = createelement(importosenzasconto,importoscontato,imponibile,imposta,aliquota,percentualesconto,valoresconto,tipodocumento) 
	current2 = createelement(importosenzasconto2,importoscontato2,imponibile2,imposta2,aliquota2,percentualesconto2,valoresconto2,tipodocumento2) 
	if(tipodocumento!="TOTALE"):
		taxs = createTAX(importoscontato,imposta,aliquota,importoscontato2,imposta2,aliquota2) 
		prev = current
		prev2 = current2
	else:	
		#print prev,prev2,current
		iva  = createiva(imposta)
		pagementoC = line[18]
		pagementoE = line[19]
		pagementoCred = line[20]
		jpagementoC = createPagContanti(pagementoC)
		jpagementoE = createPagElettronico(pagementoE)
		jpagementoCred = createPagCredito(pagementoCred)
		fiscal = createfiscaldata(amount,int(float(importoscontato.replace(",","."))*100),prev,prev2,current,iva,jpagementoC,jpagementoE,jpagementoCred,taxs,referenceClosurenumber,referenceDocnumber,doctype,z)
		if(doctype==1 ):
			amount += int(float(importoscontato.replace(",","."))*100)#int(importoscontato)

		r = dict((k, str(v).replace("'","\"")) for k, v in fiscal.iteritems())
		#print "++"+json.dumps(r["fiscalData"])
		#print json.dumps(r["fiscalData"])
		shaMetadata =  createhash(r["fiscalData"])
		print  shaMetadata
		addInfo = matricola+";"+user+";"+str(z)+";"+str(ndoc)
		print addInfo
		signaure =  hmacsha256(cashHmacKey,shaMetadata)
		qrdata =  createqrcode(shaMetadata,"",signaure)
		#r2 = {}
		r['qrData'] = qrdata
		#r2['fiscalData'] = fiscal
		#r = dict((k, str(v)) for k, v in fiscal.iteritems())
		jsonfiscal =  json.dumps(r)
		print jsonfiscal
		print hmactoccdc(signaure)
		print "#########################"
		print "#########################"
		print "#########################"
		#parse(jsonfiscal)
		re = send_post(jsonfiscal,senddoc)
		json_reponse = json.loads(re)
		resp_code = json_reponse['responseCode']
		ndoc+=1
		#print re
		cashToken = signaure	
		print "exit",ndoc
		#time.sleep(5) 
		if(int(resp_code)==1100):
			print "resp_code"+str(resp_code)
			break
		if(ndoc>=2):
			break
		#exit(0)
close = 0
if(len(sys.argv)>3):
	 close = sys.argv[3]

if (close==0):
	close_ECR_command = {"data" : { "cashuuid" : user,"znum" : z , "dtime" : date, "amount" : amount}}
	print close_ECR_command
	json_close_ECR = json.dumps(close_ECR_command)
	resp = send_post(json_close_ECR,sendZ)


exit(0)

#print taxs
exit(0)


amount = 0
znum = 0
close_ECR_command = {"data" : { "cashuuid" : user,"znum" : znum , "dtime" : date, "amount" : amount}}
json_close_ECR = json.dumps(close_ECR_command)
resp = send_post(json_close_ECR,sendZ)

print json_close_ECR
print resp
exit(0)

close_fiscalbox = {"data" : { "type" : "0"}}
json_close_fiscalbox = json.dumps(close_fiscalbox)
#respc = send_post(json_close_fiscalbox,sendzdoc)

exit(0)







ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



request = urllib2.Request('https://'+set_ip_server+'/insertFiscalDocument.php')
base64string = base64.encodestring('%s:%s' % ('userCASSA', 'PASS')).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)   

print request
response = urllib2.urlopen(request, context=ssl._create_unverified_context())

print response
exit(0)
