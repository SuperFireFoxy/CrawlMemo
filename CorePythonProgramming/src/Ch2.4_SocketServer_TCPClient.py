from socket import *

HOST = 'localhost'
PORT = 8099
BUFSIZE = 1024
ADDR = (HOST, PORT)
while True:
    tcpClientSock = socket(AF_INET, SOCK_STREAM)
    tcpClientSock.connect(ADDR)
    data = input('> ')
    if not data:
        break
    tcpClientSock.send(bytes("%s\r\n" % data, 'UTF-8'))
    data = tcpClientSock.recv(BUFSIZE)
    if not data:
        break
    print(data.strip())
    tcpClientSock.close()
