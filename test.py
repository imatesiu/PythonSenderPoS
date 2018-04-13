#!/usr/bin/python
#99SEA000217AAAA0001143902017111300270002000063570
def test():
	token = "99SEA000217AAAA0001143902017111300270002000063570"
	ndoc =  token[36:40]
	print token[32:36]
	n = int(ndoc)
	print n
	n +=100
	print str(n).zfill(4)  
	exit(0)
	return token[:44], float(token[44:])/100


from datetime import datetime
da =  datetime.now().strftime('%Y%m%dT%H%M%S')
print type(da)
exit(0)
token,dailyamount = test()
print token
print dailyamount

scontrino = "<receipt><hash fingerPrint=\""+token+"\"/><printerFiscalReceipt><beginFiscalReceipt/><printRecItem description=\"VAT ID 1\" quantity=\"1\" unitPrice=\"-10,00\" vatID=\"1\"/><printRecItem description=\"VAT ID 2\" quantity=\"1\" unitPrice=\"0,20\" vatID=\"2\"/><printRecItem description=\"VAT ID 3\" quantity=\"1\" unitPrice=\"-0,30\" vatID=\"3\"/><printRecItem description=\"VAT ID 0\" quantity=\"1\" unitPrice=\"-0,40\" vatID=\"0\"/><printRecTotal description=\"PAGAMENTO CONTANTE\" index=\"0\" payment=\"0\" paymentType=\"0\"/><fiscalInformation cashAmount=\"-10,50\" changeAmount=\"0,00\" dailyAmount=\""+str(dailyamount).replace(".",",")+"\" dateTime=\"20171023T085606\" docType=\"0\" ePayAmount=\"-10,00\" noPayAmount=\"0,00\" paidAmount=\"-10,50\" recAmount=\"-10,50\" recNumber=\"0006\" recVAT=\"-1,83\" tillId=\"AAAA0001\" zRepNumber=\"0036\"/><endFiscalReceipt/></printerFiscalReceipt></receipt>"

print scontrino