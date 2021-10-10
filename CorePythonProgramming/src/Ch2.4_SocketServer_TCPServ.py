#! /usr/bin/python
from socketserver import (StreamRequestHandler as SRH, TCPServer as TCP)
from time import ctime

HOST = ''
PORT = 8099
ADDR = (HOST, PORT)


class MyMsgHandler(SRH):
    def handle(self):
        print("....connecting from:", self.client_address)
        strResponse = '%s : %s' % (ctime(), self.rfile.readline())
        self.wfile.write(bytes(strResponse, 'utf-8'))


tcpServ = TCP(ADDR, MyMsgHandler)
print("waiting for connection....")
tcpServ.serve_forever()
