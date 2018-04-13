import requests
import time
import xml.etree.ElementTree
from datetime import datetime
from datetime import timedelta
import xml.etree.ElementTree as ET

set_ip_apparato = "192.168.0.54"

def xmltodate(xml):
	root = ET.fromstring(xml)
	a = (root.findall(".//extraInfo"))
	text = a[0].text
	datet = datetime.strptime(text, '%d%m%Y%H%M%S')
	return datet
	#print res

def dateplus(date):
	end_date = date + timedelta(days=1)
	return end_date.strftime('%d%m%Y')


def createnewdata(xml):
	da = xmltodate(xml)
	r = dateplus(da)
	print r
	data4 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><SetEcrDate><SETDATE><DATE>"+r+"</DATE><TIME>010000</TIME></SETDATE></SetEcrDate></soap:Body></soap:Envelope>"
	return data4

def send_post(content):
	response = requests.post('http://'+set_ip_apparato+':80/oli_webservice.cgi',data=content,headers={"Content-Type": "text/xml"})
	print response.text
	assert response.status_code == 200
	return response.text

documentocommerciale = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD>...<E_SALE>..<OPTYPE>1</OPTYPE>....<BARCODETYPE></BARCODETYPE>..<NUMBER>1</NUMBER>..<LISTPRICE>1</LISTPRICE>..<SALETYPE>1</SALETYPE>..<DESCRIPTION></DESCRIPTION>..<AMOUNT>1</AMOUNT>..<QUANTITY_1></QUANTITY_1>..<QUANTITY_2></QUANTITY_2>..<QUANTITY_3></QUANTITY_3>..<QUANTITY_4></QUANTITY_4>..<M_QUANTITY></M_QUANTITY>..<S_QUANTITY></S_QUANTITY>..<RAEETYPE></RAEETYPE>..<RAEEVALUE></RAEEVALUE>.</E_SALE></CMD><CMD>...<E_PAYMENT>..<P_TYPE>1</P_TYPE>...<NUMBER>1</NUMBER>...<DESCRIPTION>PAGAMENTO</DESCRIPTION>...<AMOUNT></AMOUNT>....<CUSTOMERACCOUNT></CUSTOMERACCOUNT>...</E_PAYMENT></CMD></EcrTickets></soap:Body></soap:Envelope>"

zfiscale = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><ExecuteReport>.<PRINTREP>1</PRINTREP>.<REPTYPE>1</REPTYPE>.<REPNUM>10</REPNUM>.</ExecuteReport></soap:Body></soap:Envelope>"

changedate = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets><CMD><GETDATE></GETDATE></CMD></EcrTickets></soap:Body></soap:Envelope>"

day = 6
data2 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><SetEcrDate><SETDATE><DATE>08102017</DATE><TIME>010000</TIME></SETDATE></SetEcrDate></soap:Body></soap:Envelope>"

def create_data(day):
	da = str(day).zfill(2)
	data4 = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><SetEcrDate><SETDATE><DATE>"+da+"112017</DATE><TIME>010000</TIME></SETDATE></SetEcrDate></soap:Body></soap:Envelope>"
	return data4


num = 2
while True:
	if num == 1 or num == 40:
			xml = send_post(changedate)
			d = str(xml)
			dmsg = createnewdata(d)
			send_post(dmsg)
			send_post(dmsg)
			num = 2
	send_post(documentocommerciale)
	send_post(zfiscale)
	print num
	time.sleep(200)
	num +=1
