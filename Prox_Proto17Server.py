import socket

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Ensure that you can restart your server quickly when it terminates
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set the client socket's TCP "well-known port" number
well_known_port = 12345
sock.bind(('', well_known_port))

# Set the number of clients waiting for connection that can be queued
sock.listen(5)

def calculate_LRC(data):
   lrc = 0x7F
   for element in data:
       lrc^=element
   return lrc
   
hhex = '0603'
res = bytearray.fromhex(hhex)
lrc = calculate_LRC(res)


# loop waiting for connections (terminate with Ctrl-C)
#print(bytes.fromhex(hex_val))
try:
    while 1:
        newSocket, address = sock.accept()
        print("Connected from", address)
        sock2.connect(("146.48.84.159", 12345))
        # loop serving the new client
        while 1:
            receivedData = newSocket.recv(1024)
            if not receivedData: break
            print("Ricevuti: ")
            print(receivedData)
            # Echo back the same data you just received
            
            sock2.send(receivedData)
            data = sock2.recv(1024)
            print(data)
            newSocket.send(data)
            
            
            
        newSocket.close()
        print("Disconnected from", address)
finally:
    sock.close()