import requests
import socket


#IP DEL DISPOSITIVO ESPSON RT
set_ip_server = "192.168.1.210"
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
	
#funzione per invio messaggi sulla porta 80 procollo HTTP POST
def send_post_cgi(content):
    send = bustasoap(content)
    print(send)
    response = requests.post('http://'+set_ip_server+':'+str(port_cgi)+'/cgi-bin/fpmate.cgi',data=send,headers={"Content-Type":
"application/soap+xml", "charset":
"utf-8" })
    print(response.text)
    assert response.status_code == 200
    return response.text

#funzione per inserire in una busta SOAP i messaggi inviati
def bustasoap(content):
    soap = "<?xml version=\"1.0\" encoding=\"utf-8\"?><soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"><soapenv:Body>"+content+"</soapenv:Body></soapenv:Envelope>"
    return soap
    
#varibile contentente DC Pagamento Elettronico 8 con codice lotteria (FPMATE03) da PC (protocollo FpMate CGI)
Lotteria = "<printerFiscalReceipt><beginFiscalReceipt operator=\"1\" /><printRecItem operator=\"1\" description=\"PANINO\" quantity=\"1\" unitPrice=\"8\" department=\"1\" justification=\"1\"/><printRecLotteryID operator=\"1\" code=\"FPMATE03\"  /><printRecTotal operator=\"1\"description=\"Payment Bancomat\" payment=\"8\" paymentType=\"2  \" index=\"1\" justification=\"1\"/><endFiscalReceipt  operator=\"1\" /></printerFiscalReceipt>"
#varibile contentente DC Pagamento Elettronico 3 senza codice lotteria da PC (protocollo FpMate CGI)
NOLotteria = "<printerFiscalReceipt><beginFiscalReceipt  operator=\"1\" /><printRecItem operator=\"1\" description=\"PANINO2\" quantity=\"1\" unitPrice=\"3\" department=\"1\" justification=\"1\"/><printRecTotal operator=\"1\" description=\"Payment Bancomat\" payment=\"3\" paymentType=\"2\"index=\"1\" justification=\"1\" /><endFiscalReceipt  operator=\"1\" /></printerFiscalReceipt>"

#Comando leggi memoria permanente di dettaglio per data
readEJ = "<printerCommand><queryContentByDate operator=\"1\" dataType=\"0\" fromDay=\"15\" fromMonth=\"12\" fromYear=\"2023\" toDay=\"15\" toMonth=\"12\" toYear=\"2023\" /><printerCommand>"
#Comando leggi memoria permanente di dettaglio per data e numero documento
readEJDay = "<printerCommand><queryContentByNumbers operator=\"1\" dataType=\"0\" day=\"15\" month=\"12\" year=\"2023\" fromNumber=\"3\" toNumber=\"23\" /> </printerCommand>"

#Emissione DC Pagamento Elettronico 2 senza codice lotteria da PC (protocollo EPOS Fiscal)
rep1hex  = '02303345313038303031312078203220524550203130303031303030303030303030323030303131313003' 
#03E1080011 x 7 REP 1000100000000070001120

pagehex  = '023032453130383430314361727461206469204372656469746f203130303030303030303032303131353203' 
#02E108401Carta di Credito 1000000000201152

#send9100(rep1hex.decode('hex'))
#send9100(pagehex.decode('hex'))


#Emissione DC Pagamento Elettronico 7 con codice lotteria (EPOS0002) da PC (protocollo EPOS Fiscal)
rep2h = '02303345313038303031312078203720524550203130303031303030303030303030373030303131323003' 
#03E1080011 x 7 REP 1000100000000070001120

                            #45504f5330303032 = EPOS0002
loth =  '0230324531313335303145504f5330303032202020202020202030303030313903' #02E113501EPOS0002        000019
pageh = '0230334531303834303145504f533030303230303030303030303032303131303303' 
#03E108401EPOS0002000000000201103

#print send9100(rep2h.decode('hex'))
#print send9100(loth.decode('hex'))
#print send9100(pageh.decode('hex'))

#Emissione DC Pagamento Elettronico 8 con codice lotteria (FPMATE03) da PC (protocollo FpMate CGI)
send_post_cgi(Lotteria)

#Emissione DC Pagamento Elettronico 3 senza codice lotteria da PC (protocollo FpMate CGI)
#send_post_cgi(NOLotteria)



#Emissione DC Pagamento Elettronico 4,00 senza codice lotteria da PC (protocollo XON-XOFF)
#send9100(b'\"VENDITA\"400H1R')
#send9100(b'\"PAGAMENTO ELETTRONICO\"201T')

#Emissione DC Pagamento Elettronico 4,50 con codice lotteria (XONXOFF4) da PC (protocollo XON-XOFF)
#send9100(b'\"VENDITA\"450H1R')
#send9100(b'\"XONXOFF4\"@39F')
#send9100(b'\"PAGAMENTO ELETTRONICO\"201T')

#send_post_cgi(readEJDay)
