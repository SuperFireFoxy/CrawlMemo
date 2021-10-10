#! /usr/bin/python
from time import ctime

from twisted.internet import protocol, reactor

PORT = 8099


class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print("......connection from: %s", clnt)

    def dataReceived(self, data):
        self.transport.write(('[%s] %s' % (ctime(), data)).encode())


factory = protocol.Factory()
factory.protocol = TSServProtocol
print('.....waiting for connection.....')
reactor.listenTCP(PORT, factory)
reactor.run()
