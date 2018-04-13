import requests


def send_post(content):
	#response = requests.post('http://192.168.1.146:9090/dispositivi/corrispettivi/',data=content,headers={"Content-Type": "application/xml"}, verify=False)
	pem = 'cert.key'
	response = requests.post('https://192.168.1.146:7443/dispositivi/corrispettivi/',data=content,headers={"Content-Type": "application/xml"}, verify=pem)
	print response.text
	assert response.status_code == 200

content = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?> <ns2:DatiCorrispettivi xmlns:ns2=\"http://ivaservizi.agenziaentrate.gov.it/docs/xsd/corrispettivi/dati/v1.0\">    <Trasmissione>        <Progressivo>56</Progressivo>        <Formato>COR10</Formato>    </Trasmissione>    <DataOraRilevazione>2017-03-17T15:38:16</DataOraRilevazione>    <DatiRT>        <Riepilogo>            <IVA>                <AliquotaIVA>10.00</AliquotaIVA>                <Imposta>1.00</Imposta>            </IVA>            <Ammontare>10.00</Ammontare>        </Riepilogo>    </DatiRT></ns2:DatiCorrispettivi>"

send_post(content)

