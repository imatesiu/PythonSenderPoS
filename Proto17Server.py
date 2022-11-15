import socket
import time

from datetime import date

from time import sleep


# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ensure that you can restart your server quickly when it terminates
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set the client socket's TCP "well-known port" number
well_known_port = 1000
sock.bind(('', well_known_port))

# Set the number of clients waiting for connection that can be queued
sock.listen(5)

def calculate_LRC(data):
   lrc = 0x7F
   for element in data:
       lrc^=element
   return lrc
   
hhex = '0231303030303130353053202020546573746174612073636F6E7472696E6F2020202020202020202020204D41455354524F2020202020202020202020202020204D41455354524F43484950202020202020207F2020202020202020414351554953544F20202020202020202020202020494E47454E49434F2020202020202020202020202020202020202056495341564953412020202020202020202020202003'
res = bytearray.fromhex(hhex)
lrc = calculate_LRC(res)
#g = bytearray.fromhex(hhex+str(lrc))
print(hex(lrc))

#exit(0)

def calcstanslim(stan,importo):
    tempodata = time.strftime("%d/%m/%y").encode('utf-8')
    tempoora = time.strftime("%H:%M").encode('utf-8')
    sst = format(stan, '06').encode('utf-8')
    pre = "0231303030303233353053202020202020204d41535445524341524420202020202020202020204d415354455243415244204348495020202020207f2020202020202020414351554953544f2020202020202020202020202020434E522053534520202020202020202020202043524544495420434152442020202020202020202020202020202020202020202020202020202020202045736572632e202020202020303030303030333030323331412e492e492e432e202020202038383130353130303030344461746120"
    hexdata = tempodata.hex()
    pre = pre + hexdata +'20204F726120'
    hexora = tempoora.hex()
    pre = pre + hexora + '544D4C203130303030313035205354414E20'
    hexsst = sst.hex()
    pre = pre + hexsst + '4D6F642E204F6E6C696E652020202020422E432E204943434155542E20313531333620204F5045522E20303030313032415554482E524553502E434F44452020202020202020303050414E20202020202A2A2A2A2A2A2A2A2A2A2A2A3535343153434144202020202020202020202020202020202A2A2A2A43564D2050696E204F66666C696E652020202020202020202020202020202020202020202020202020202020202020207F494D504F52544F20455552202020202020202020'
    numStr = importo.rjust(8, ' ')
    if(len(importo)==5):
       numStr = importo.rjust(8, ' ')
    if(len(importo)==6):
       numStr = importo.rjust(7, ' ')
    if(len(importo)==4):
       numStr = importo.rjust(9, ' ')
    simponto = numStr.encode('utf-8').hex()
    pre = pre + simponto + "202020202020202020202020202020202020202020202020205452414e53415a494f4e4520415050524f564154412020202020202020202020202020202020202020202020202020202020202020"
    res = bytearray.fromhex(pre)
    lrc = str(hex(calculate_LRC(res)))[2:4]
    pre = pre + lrc
    return pre

def calcstan(stan):
    tempodata = time.strftime("%d/%m/%y").encode('utf-8')
    tempoora = time.strftime("%H:%M").encode('utf-8')
    sst = format(stan, '06').encode('utf-8')
    
    pre = '02313030303031303530532020202020202020202020202020202020202045736572632E202020202020303030303030333030313035412E492E492E432E202020202038383130353130303036364461746120'
    hexdata = tempodata.hex()
    pre = pre + hexdata +'20204F726120'
    hexora = tempoora.hex()
    pre = pre + hexora + '544D4C203130303030313035205354414E20'
    hexsst = sst.hex()
    #pre = pre + hexsst + '4D6F642E204F6E6C696E652020202020422E432E204943434155542E2037333039362003'
    pre = pre + hexsst + '4D6F642E205A4F6E6C696E3320202020422E432E204943434155542E2037333039362003'
    res = bytearray.fromhex(pre)
    lrc = str(hex(calculate_LRC(res)))[2:4]
    pre = pre + lrc
    return pre
    
def calcpan(importo):
    numStr = importo.rjust(8, ' ')
    if(len(importo)==5):
       numStr = importo.rjust(8, ' ')
    if(len(importo)==6):
       numStr = importo.rjust(7, ' ')
    if(len(importo)==4):
       numStr = importo.rjust(9, ' ')
    #print(numStr)
    simponto = numStr.encode('utf-8').hex()
    print(simponto)
    #pre = '023130303030313035305320202020202020202020202020415554482E524553502E434F44452020202020202020303050414E20202020203637363231302A2A2A2A2A2A3539343943564D2050696E204F6E6C696E65202020202020202020202020202020202020202020202020202020202020202020207F494D504F52544F2045555220202020'
    pre = '023130303030313035305320202020202020202020202020415554482E524553502E434F44452020202020202020303050414E20202020203637363231302A2A2A2A2A2A3539343943564D2050696E20306E6C696E33202020202020202020202020202020202020202020202020202020202020202020207F494D504F52544F2045555220202020'    
    pre = pre + simponto + '2020202020202020202020202020202003'
    res = bytearray.fromhex(pre)
    lrc = str(hex(calculate_LRC(res)))[2:4]
    pre = pre + lrc
    return pre
    
def calfine():
    pre = '02313030303031303530532020202020202020205452414E53415A494F4E4520415050524F564154412020202020202020202020202020202020202020202020202020202041525249564544455243492045204752415A494520202046696E6520726963657675746120706167616D656E746F207D7D1B03'
    res = bytearray.fromhex(pre)
    lrc = str(hex(calculate_LRC(res)))[2:4]
    pre = pre + lrc
    return pre

def calfineslim():
    pre = "02313030303032333530532020474f4f442042594520202020202020207d7d1b037e"
    return pre
    
def getimporto(barray):
    h = barray.hex()
    importo = h[42:64]
    print(importo)
    imp  =  bytearray.fromhex(importo).decode("ASCII").rstrip('\x00').lstrip('0')
    if not imp:
        imp = "0,00"
        return imp
    r = imp[0:len(imp)-2]+","+imp[len(imp)-2:]
    return r
    
def getimportoPax(barray):
    h = barray.hex()
    print(h)
    importo = h[128:136]
    print(importo)
    imp  =  bytearray.fromhex(importo).decode("ASCII").rstrip('\x00').lstrip('0')
    if not imp:
        imp = "0,00"
        return imp
    r = imp[0:len(imp)-2]+","+imp[len(imp)-2:]
    return r
  

def calcpan_pax(stan):
    tempoora = time.strftime("%H%M").encode('utf-8').hex()
    #print(tempoora)
    today = date.today()
    d1 = date(2022, 1, 1)
    delta = today - d1 
    nd = delta.days + 1
    asd = str(nd).rjust(3, '0')
    ndhex = asd.encode('utf-8').hex()
    sst = format(stan, '03').encode('utf-8').hex()
    #print('sst:'+sst)
    #pre = '023130303030313035305320202020202020202020202020415554482E524553502E434F44452020202020202020303050414E20202020203637363231302A2A2A2A2A2A3539343943564D2050696E204F6E6C696E65202020202020202020202020202020202020202020202020202020202020202020207F494D504F52544F2045555220202020'
    pre = '0231303030303135323045303030303035333434313330303030303039353833434C49353334333435'
    
      
    pre = pre + ndhex + tempoora + '323838313035303030303034303030'+sst+'30303030343503'
    res = bytearray.fromhex(pre)
    lrc = str(hex(calculate_LRC(res)))[2:4]
    pre = pre + lrc
    print(pre)
    return pre 
  
    
    
    
shex  = '0230303030303030303058202020202020202030303030303530300000000000202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202030303030303030300313'
shex2 = '0230303030303030303058202020202020202030303030303535343035000000202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202030303030303030300317'
shex3 = '0230303030303030303058202020202020202030303030303130350000000000202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202030303030303030300312'
shex4 = '0230303030303030303058202020202020202030303030303030300000000000202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202030303030303030300316'
#print("s "+shex[38:54])
shex = '0231303030303135323045303030303035333434313330303030303039353833434C4935333433343530353531303433323838313035303030303034303030303131303030303435034C'
r = getimportoPax(bytearray.fromhex(shex))   
print(calcpan_pax(22))
#print(r)

#r = getimporto(bytearray.fromhex(shex2))   
#print(r)

#r = getimporto(bytearray.fromhex(shex3))   
#print(r)

#r = getimporto(bytearray.fromhex(shex4))   
#print(r)
#print(calcpan(1))
#exit(0)    
#print(calcstan(23))
#print(float("0022,00".replace(",",".")))
#print(calcpan("2,00"))
#cpan = bytearray.fromhex(calcpan("2,00"))
#print(cpan)
#exit(0)
stanstan = 30
pax = False
# loop waiting for connections (terminate with Ctrl-C)
#print(bytes.fromhex(hex_val))
try:
    while 1:
        newSocket, address = sock.accept()
        print("Connected from", address)
        # loop serving the new client
        while 1:
            stanstan+=10
            receivedData = newSocket.recv(2048)
            if not receivedData: break
            print("Ricevuti: ")
            print(receivedData)
            # Echo back the same data you just received 023030303030303030304531033a
            ingenicaoinit      =  bytearray.fromhex('023030303030303030304531033a')
            ingenicaoinitslim  =  bytearray.fromhex('023130303030323335304531033f')
            ack = bytearray.fromhex('06037A')
            statuspos =  bytearray.fromhex('0200000000000000003074033A')
            wait = bytearray.fromhex('01003A')
            
            operazioneincorso = bytearray.fromhex('014f504552415a494f4e4520494e20434f52534f2004')
            opok = bytearray.fromhex('023130303030313035304530303030303637363231302a2a2a2a2a2a35393439494343373330393620303333303831353238383130353130303036363030303133303030303137343030303030303030313030303030303030303030300363')
            
            
            newSocket.send(ack)
            
            
            opok_pax = bytearray.fromhex('0231303030303135323045303030303035333434313330303030303039353833434C4935333433343530353531303433323838313035303030303034303030303131303030303435034C')

            if(len(receivedData)!=len(ingenicaoinit)):
                r = getimportoPax(receivedData)
                print(r)
                newSocket.send(bytearray.fromhex(calcpan_pax(stanstan)))
                pax = True
                #newSocket.send(opok_pax)
            
            opko = bytearray.fromhex('023130303030313035304530315452414e53415a494f4e452052494649555441544120202030303030303030303030303138383130353130303030313030303133333030303137373930373030303030313030303030303030303030300308')
            
            
            
            receivedData = newSocket.recv(1024)
            if not receivedData: break
            print("Ricevuti2: ")
            print(receivedData.hex())
            
            r = getimporto(bytearray(receivedData))    
            print(r)
            
            newSocket.send(ack)
            newSocket.send(operazioneincorso)
            #
            sleep (2)
            if(pax):
                newSocket.send(opok_pax)
            else:
                newSocket.send(opok)
            receivedData = newSocket.recv(1024)
            if not receivedData: break
            print("Ricevuti3: ")
            print(receivedData)
            
            testata = bytearray.fromhex('0231303030303130353053202020546573746174612073636F6E7472696E6F2020202020202020202020204D41455354524F2020202020202020202020202020204D41455354524F43484950202020202020207F2020202020202020414351554953544F20202020202020202020202020494E47454E49434F202020202020202020202020202020202020205649534156495341202020202020202020202020200361')
            
            testatako=bytearray.fromhex('0231303030303130353053202020546573746174612073636f6e7472696e6f202020202020202020205041474f42414e434f4d41542020202020202020202020202020504220434849502020202020202020207f2020202020202020414351554953544f20202020202020202020202020494e47454e49434f205445535420202020202020202020202020204f4c495645545449202020202020202020202020200375')
            
            newSocket.send(testata)
            
            receivedData = newSocket.recv(2048)
            if not receivedData: break
            print("Ricevuti4: ")
            print(receivedData)
            
            #stan = bytearray.fromhex('02313030303031303530532020202020202020202020202020202020202045736572632e202020202020303030303030333030313035412e492e492e432e20202020203838313035313030303636446174612030322f30322f323220204f72612030383a3135544d4c203130303030313035205354414e203030303133304d6f642e204f6e6c696e652020202020422e432e204943434155542e20373330393620031e')
            
            #stan = bytearray.fromhex('02313030303031303530532020202020202020202020202020202020202045736572632e202020202020303030303030333030313035412e492e492e432e20202020203838313035313030303636446174612030322f30322f323220204f72612030383a3135544d4c203130303030313035205354414e203030303133304d6f642e204f6e6c696e652020202020422e432e204943434155542e20373330393620031e')
            
            dec_stan = bytearray.fromhex('02313030303031303530532020202020202020202020202020202020202045736572632e202020202020303030303030333030313035412e492e492e432e20202020203838313035313030303031446174612030322f30322f323220204f72612031313a3038544d4c203130303030313035205354414e203030303133334d6f642e204f6e6c696e652020202020422e432e20494343412e432e203930372020200371')
            
            cstan = bytearray.fromhex(calcstan(stanstan))
            
            newSocket.send(cstan)
            
            receivedData = newSocket.recv(1024)
            if not receivedData: break
            print("Ricevuti5: ")
            print(receivedData)
            
            pan = bytearray.fromhex('023130303030313035305320202020202020202020202020415554482e524553502e434f44452020202020202020303050414e20202020203637363231302a2a2a2a2a2a3539343943564d2050696e204f6e6c696e65202020202020202020202020202020202020202020202020202020202020202020207f494d504f52544f20455552202020202020202020312c3030202020202020202020202020202020200301')
            
            panko = bytearray.fromhex('0231303030303130353053204f5045522e20303030313737202020202020202020202020202020202020202020202020494d504f52544f20455552202020202020202020312c30303d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d7f20202020202020204445434c494e454420202020202020202020202049535355455220494e4f50455241542e202020203d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d035a')
            
            cpan = bytearray.fromhex(calcpan(r))
            
            newSocket.send(cpan)
            receivedData = newSocket.recv(1024)
            if not receivedData: break
            print("Ricevuti6: ")
            print(receivedData)
            
            fine = bytearray.fromhex('02313030303031303530532020202020202020205452414e53415a494f4e4520415050524f564154412020202020202020202020202020202020202020202020202020202041525249564544455243492045204752415a49452020202020202046696e652073636f6e7472696e6f20202020207d7d1b036f')
            dec_fine = bytearray.fromhex('02313030303031303530533d3d3d3d3d3d3d3d202020202046696e652073636f6e7472696e6f20202020207d7d1b0378')

            cfine = bytearray.fromhex(calfine())
            
            newSocket.send(cfine)
            receivedData = newSocket.recv(1024)
            if not receivedData: break
            print("Ricevuti7: ")
            print(receivedData)
            
            
        newSocket.close()
        print("Disconnected from", address)
finally:
    sock.close()