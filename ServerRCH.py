#!/usr/bin/python
import socket 
import time



from http.server import HTTPServer, BaseHTTPRequestHandler

import ssl

from io import BytesIO


class SimpleHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        #self.wfile.write(b'Hello, world!')
        self.wfile.write(b'{"error_code":"150","error_mesg":"Richiesta non valida"}')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'{"error_code":"150","error_mesg":"Richiesta non valida"}')
        #response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

httpd = HTTPServer(('localhost', 4443), SimpleHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='/Users/spagnolo/github/PythonSenderPoS/server.cer', keyfile='/Users/spagnolo/github/PythonSenderPoS/server.key' ,server_side=True)
httpd.serve_forever()