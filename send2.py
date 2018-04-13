#!/usr/bin/python
import xml.etree.ElementTree
from datetime import datetime
from datetime import timedelta

getdate  = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><soap:Envelope xmlns:soap=\"http://www.w3.org/2001/12/soap-envelope\"><soap:Body><EcrTickets>	<ActionResultCode>1000</ActionResultCode>	<ActionResultStr>Comando eseguito con successo.</ActionResultStr>	<cmdResult>		<cmdIndex>0</cmdIndex>		<cmdCode>GETDATE</cmdCode>		<resCode>1000</resCode>		<extraInfo>09112017012903</extraInfo>	</cmdResult></EcrTickets></soap:Body></soap:Envelope>"

import xml.etree.ElementTree as ET
#root = ET.fromstring(getdate)

#a = (root.findall(".//extraInfo"))
#print a[0].text


def xmltodate(xml):
	root = ET.fromstring(getdate)
	a = (root.findall(".//extraInfo"))
	text = a[0].text
	datet = datetime.strptime(text, '%d%m%Y%H%M%S')
	return datet
	#print res
	
def dateplus(date):
	end_date = date + timedelta(days=1)
	return end_date.strftime('%d%m%Y%H%M%S')
	


res = xmltodate(getdate)
end_date = dateplus(res)


print end_date


