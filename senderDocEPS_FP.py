import requests
import socket
import time

#IP DEL DISPOSITIVO ESPSON RT
set_ip_server = "146.48.84.159"
port = 9100
port_cgi = 80

#funzione per invio messaggi sulla porta 9100 socket TCP
def send9100(msg):
  try:
    opened_socket2 = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    opened_socket2.connect((set_ip_server, port))
    print(msg)
    r = opened_socket2.send(msg)
    #data = opened_socket2.recv(1024).decode()
    #print(data)
    opened_socket2.close()
    return r
  except Exception as e:
      print(str(e))
	
	
#funzione per invio messaggi sulla porta 80 protocollo HTTP POST
def send_post_cgi(content):
    send = bustasoap(content)
    print(send)
    response = requests.post('http://'+set_ip_server+':'+str(port_cgi)+'/cgi-bin/fpmate.cgi',data=send,headers={"Content-Type": "application/soap+xml", "charset":
"utf-8" })
    print(response.text)
    assert response.status_code == 200
    return response.text

#funzione per inserire in una busta SOAP i messaggi inviati
def bustasoap(content):
    soap = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body>"+content+"</soapenv:Body></soapenv:Envelope>"
    return soap
    

#varibile contentente DC Pagamento Elettronico 3 senza codice lotteria da PC (protocollo FpMate CGI)
NOLotteria = "<printerFiscalReceipt><beginFiscalReceipt  operator=\"1\" /><printRecItem operator=\"1\" description=\"PANINO2\" quantity=\"1\" unitPrice=\"3\" department=\"1\" justification=\"1\" /><printRecTotal operator=\"1\" description=\"Payment Bancomat\" payment=\"3\" paymentType=\"2\" index=\"1\" justification=\"1\" /><endFiscalReceipt  operator=\"1\" /></printerFiscalReceipt>"

#Comando leggi memoria permanente di dettaglio per data
chiusuraRT = "<printerFiscalReport><printZReport operator=\"1\" /></printerFiscalReport>"


for i in range(3):
    send9100(b'\"VENDITA\"400H1R')
    send9100(b'\"PAGAMENTO CONTANTE\"1T')
    send9100(b'1F')
    time.sleep(5)
    print i

#Emissione DC Pagamento Elettronico 3 senza codice lotteria da PC (protocollo FpMate CGI)
#send_post_cgi(NOLotteria)

#send_post_cgi(chiusuraRT)



'''

#Attivazione FLAG 35 del SET14 protocollo XON-XOFF
set14351 = '0230324534303134333531323103' #SET14 FLAG 35 VAL 1 Attivo
print send9100(set14351.decode('hex'))

#Emissione DC Pagamento Elettronico 4,00 senza codice lotteria da PC (protocollo XON-XOFF)
send9100(b'\"VENDITA\"400H1R')
send9100(b'\"PAGAMENTO ELETTRONICO\"201T')

#Emissione DC Pagamento Elettronico 4,50 con codice lotteria (XONXOFF4) da PC (protocollo XON-XOFF)
send9100(b'\"VENDITA\"450H1R')
send9100(b'\"XONXOFF4\"@39F')
send9100(b'\"PAGAMENTO ELETTRONICO\"201T')

#Disattivazione FLAG 35 del SET14 protocollo XON-XOFF
set14350 = '0230324534303134333530323103' #SET14 FLAG 35 VAL 0 Disattivo
print send9100(set14350.decode('hex'))
syncEpsPro = '31343932450230314534323031363503' #1492E
print send9100(syncEpsPro.decode('hex'))
#send_post_cgi(readEJDay)'''
